#![cfg(feature = "macros")]

#[cfg(not(Py_LIMITED_API))]
use pyo3::buffer::PyBuffer;
use pyo3::prelude::*;
use pyo3::types::{self, PyCFunction};
#[cfg(not(Py_LIMITED_API))]
use pyo3::types::{PyDateTime, PyFunction};

mod common;

#[pyfunction(arg = "true")]
fn optional_bool(arg: Option<bool>) -> String {
    format!("{:?}", arg)
}

#[test]
fn test_optional_bool() {
    // Regression test for issue #932
    let gil = Python::acquire_gil();
    let py = gil.python();
    let f = wrap_pyfunction!(optional_bool)(py).unwrap();

    py_assert!(py, f, "f() == 'Some(true)'");
    py_assert!(py, f, "f(True) == 'Some(true)'");
    py_assert!(py, f, "f(False) == 'Some(false)'");
    py_assert!(py, f, "f(None) == 'None'");
}

#[cfg(not(Py_LIMITED_API))]
#[pyfunction]
fn buffer_inplace_add(py: Python, x: PyBuffer<i32>, y: PyBuffer<i32>) {
    let x = x.as_mut_slice(py).unwrap();
    let y = y.as_slice(py).unwrap();
    for (xi, yi) in x.iter().zip(y) {
        let xi_plus_yi = xi.get() + yi.get();
        xi.set(xi_plus_yi);
    }
}

#[cfg(not(Py_LIMITED_API))]
#[test]
fn test_buffer_add() {
    let gil = Python::acquire_gil();
    let py = gil.python();
    let f = wrap_pyfunction!(buffer_inplace_add)(py).unwrap();

    py_expect_exception!(
        py,
        f,
        r#"
import array
a = array.array("i", [0, 1, 2, 3])
b = array.array("I", [0, 1, 2, 3])
f(a, b)
"#,
        PyBufferError
    );

    pyo3::py_run!(
        py,
        f,
        r#"
import array
a = array.array("i", [0, 1, 2, 3])
b = array.array("i", [2, 3, 4, 5])
f(a, b)
assert a, array.array("i", [2, 4, 6, 8])
"#
    );
}

#[cfg(not(Py_LIMITED_API))]
#[pyfunction]
fn function_with_pyfunction_arg(fun: &PyFunction) -> PyResult<&PyAny> {
    fun.call((), None)
}

#[pyfunction]
fn function_with_pycfunction_arg(fun: &PyCFunction) -> PyResult<&PyAny> {
    fun.call((), None)
}

#[test]
fn test_functions_with_function_args() {
    let gil = Python::acquire_gil();
    let py = gil.python();
    let py_cfunc_arg = wrap_pyfunction!(function_with_pycfunction_arg)(py).unwrap();
    let bool_to_string = wrap_pyfunction!(optional_bool)(py).unwrap();

    pyo3::py_run!(
        py,
        py_cfunc_arg
        bool_to_string,
        r#"
        assert py_cfunc_arg(bool_to_string) == "Some(true)"
        "#
    );

    #[cfg(not(Py_LIMITED_API))]
    {
        let py_func_arg = wrap_pyfunction!(function_with_pyfunction_arg)(py).unwrap();

        pyo3::py_run!(
            py,
            py_func_arg,
            r#"
            def foo(): return "bar"
            assert py_func_arg(foo) == "bar"
            "#
        );
    }
}

#[cfg(not(Py_LIMITED_API))]
fn datetime_to_timestamp(dt: &PyAny) -> PyResult<i64> {
    let dt: &PyDateTime = dt.extract()?;
    let ts: f64 = dt.call_method0("timestamp")?.extract()?;

    Ok(ts as i64)
}

#[cfg(not(Py_LIMITED_API))]
#[pyfunction]
fn function_with_custom_conversion(
    #[pyo3(from_py_with = "datetime_to_timestamp")] timestamp: i64,
) -> i64 {
    timestamp
}

#[cfg(not(Py_LIMITED_API))]
#[test]
fn test_function_with_custom_conversion() {
    let gil = Python::acquire_gil();
    let py = gil.python();

    let custom_conv_func = wrap_pyfunction!(function_with_custom_conversion)(py).unwrap();

    pyo3::py_run!(
        py,
        custom_conv_func,
        r#"
        import datetime

        dt = datetime.datetime.fromtimestamp(1612040400)
        assert custom_conv_func(dt) == 1612040400
        "#
    )
}

#[cfg(not(Py_LIMITED_API))]
#[test]
fn test_function_with_custom_conversion_error() {
    let gil = Python::acquire_gil();
    let py = gil.python();

    let custom_conv_func = wrap_pyfunction!(function_with_custom_conversion)(py).unwrap();

    py_expect_exception!(
        py,
        custom_conv_func,
        "custom_conv_func(['a'])",
        PyTypeError,
        "argument 'timestamp': 'list' object cannot be converted to 'PyDateTime'"
    );
}

#[pyclass]
#[derive(Debug, FromPyObject)]
struct ValueClass {
    #[pyo3(get)]
    value: usize,
}

#[pyfunction]
fn conversion_error(
    str_arg: &str,
    int_arg: i64,
    tuple_arg: (&str, f64),
    option_arg: Option<i64>,
    struct_arg: Option<ValueClass>,
) {
    println!(
        "{:?} {:?} {:?} {:?} {:?}",
        str_arg, int_arg, tuple_arg, option_arg, struct_arg
    );
}

#[test]
fn test_conversion_error() {
    let gil = Python::acquire_gil();
    let py = gil.python();

    let conversion_error = wrap_pyfunction!(conversion_error)(py).unwrap();
    py_expect_exception!(
        py,
        conversion_error,
        "conversion_error(None, None, None, None, None)",
        PyTypeError,
        "argument 'str_arg': 'NoneType' object cannot be converted to 'PyString'"
    );
    py_expect_exception!(
        py,
        conversion_error,
        "conversion_error(100, None, None, None, None)",
        PyTypeError,
        "argument 'str_arg': 'int' object cannot be converted to 'PyString'"
    );
    py_expect_exception!(
        py,
        conversion_error,
        "conversion_error('string1', 'string2', None, None, None)",
        PyTypeError,
        "argument 'int_arg': 'str' object cannot be interpreted as an integer"
    );
    py_expect_exception!(
        py,
        conversion_error,
        "conversion_error('string1', -100, 'string2', None, None)",
        PyTypeError,
        "argument 'tuple_arg': 'str' object cannot be converted to 'PyTuple'"
    );
    py_expect_exception!(
        py,
        conversion_error,
        "conversion_error('string1', -100, ('string2', 10.), 'string3', None)",
        PyTypeError,
        "argument 'option_arg': 'str' object cannot be interpreted as an integer"
    );
    let exception = py_expect_exception!(
        py,
        conversion_error,
        "
class ValueClass:
    def __init__(self, value):
        self.value = value
conversion_error('string1', -100, ('string2', 10.), None, ValueClass(\"no_expected_type\"))",
        PyTypeError
    );
    assert_eq!(
        extract_traceback(py, exception),
        "TypeError: argument 'struct_arg': failed to \
    extract field ValueClass.value: TypeError: 'str' object cannot be interpreted as an integer"
    );

    let exception = py_expect_exception!(
        py,
        conversion_error,
        "
class ValueClass:
    def __init__(self, value):
        self.value = value
conversion_error('string1', -100, ('string2', 10.), None, ValueClass(-5))",
        PyTypeError
    );
    assert_eq!(
        extract_traceback(py, exception),
        "TypeError: argument 'struct_arg': failed to \
    extract field ValueClass.value: OverflowError: can't convert negative int to unsigned"
    );
}

/// Helper function that concatenates the error message from
/// each error in the traceback into a single string that can
/// be tested.
fn extract_traceback(py: Python, mut error: PyErr) -> String {
    let mut error_msg = error.to_string();
    while let Some(cause) = error.cause(py) {
        error_msg.push_str(": ");
        error_msg.push_str(&cause.to_string());
        error = cause
    }
    error_msg
}

#[test]
fn test_closure() {
    let gil = Python::acquire_gil();
    let py = gil.python();

    let f = |args: &types::PyTuple, _kwargs: Option<&types::PyDict>| -> PyResult<_> {
        let gil = Python::acquire_gil();
        let py = gil.python();
        let res: Vec<_> = args
            .iter()
            .map(|elem| {
                if let Ok(i) = elem.extract::<i64>() {
                    (i + 1).into_py(py)
                } else if let Ok(f) = elem.extract::<f64>() {
                    (2. * f).into_py(py)
                } else if let Ok(mut s) = elem.extract::<String>() {
                    s.push_str("-py");
                    s.into_py(py)
                } else {
                    panic!("unexpected argument type for {:?}", elem)
                }
            })
            .collect();
        Ok(res)
    };
    let closure_py = PyCFunction::new_closure(f, py).unwrap();

    py_assert!(py, closure_py, "closure_py(42) == [43]");
    py_assert!(
        py,
        closure_py,
        "closure_py(42, 3.14, 'foo') == [43, 6.28, 'foo-py']"
    );
}

#[test]
fn test_closure_counter() {
    let gil = Python::acquire_gil();
    let py = gil.python();

    let counter = std::cell::RefCell::new(0);
    let counter_fn =
        move |_args: &types::PyTuple, _kwargs: Option<&types::PyDict>| -> PyResult<i32> {
            let mut counter = counter.borrow_mut();
            *counter += 1;
            Ok(*counter)
        };
    let counter_py = PyCFunction::new_closure(counter_fn, py).unwrap();

    py_assert!(py, counter_py, "counter_py() == 1");
    py_assert!(py, counter_py, "counter_py() == 2");
    py_assert!(py, counter_py, "counter_py() == 3");
}

#[test]
fn use_pyfunction() {
    mod function_in_module {
        use pyo3::prelude::*;

        #[pyfunction]
        pub fn foo(x: i32) -> i32 {
            x
        }
    }

    Python::with_gil(|py| {
        use function_in_module::foo;

        // check imported name can be wrapped
        let f = wrap_pyfunction!(foo, py).unwrap();
        assert_eq!(f.call1((5,)).unwrap().extract::<i32>().unwrap(), 5);
        assert_eq!(f.call1((42,)).unwrap().extract::<i32>().unwrap(), 42);

        // check path import can be wrapped
        let f2 = wrap_pyfunction!(function_in_module::foo, py).unwrap();
        assert_eq!(f2.call1((5,)).unwrap().extract::<i32>().unwrap(), 5);
        assert_eq!(f2.call1((42,)).unwrap().extract::<i32>().unwrap(), 42);
    })
}

#[test]
fn required_argument_after_option() {
    #[pyfunction]
    pub fn foo(x: Option<i32>, y: i32) -> i32 {
        y + x.unwrap_or_default()
    }

    Python::with_gil(|py| {
        let f = wrap_pyfunction!(foo, py).unwrap();

        // it is an error to call this function with no arguments
        py_expect_exception!(
            py,
            f,
            "f()",
            PyTypeError,
            "foo() missing 2 required positional arguments: 'x' and 'y'"
        );

        // it is an error to call this function with one argument
        py_expect_exception!(
            py,
            f,
            "f(None)",
            PyTypeError,
            "foo() missing 1 required positional argument: 'y'"
        );

        // ok to call with two arguments
        py_assert!(py, f, "f(None, 5) == 5");

        // ok to call with keyword arguments
        py_assert!(py, f, "f(x=None, y=5) == 5");
    })
}

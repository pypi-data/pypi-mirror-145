//#![feature(trace_macros)]
#![allow(dead_code)]
#![cfg_attr(feature = "cargo-clippy", allow(redundant_closure))]

#[macro_use]
extern crate nom;

use nom::{space, Err, IResult, Needed, ErrorKind, le_u64, is_digit};
use nom::types::{CompleteStr, CompleteByteSlice};

#[allow(dead_code)]
struct Range {
  start: char,
  end: char,
}

pub fn take_char(input: &[u8]) -> IResult<&[u8], char> {
  if !input.is_empty() {
    Ok((&input[1..], input[0] as char))
  } else {
    Err(Err::Incomplete(Needed::Size(1)))
  }
}

//trace_macros!(true);

#[allow(dead_code)]
named!(range<&[u8], Range>,
    alt!(
        do_parse!(
            start: take_char >>
            tag!("-")        >>
            end: take_char   >>
            (Range {
                start: start,
                end:   end,
            })
        ) |
        map!(
            take_char,
            |c| {
                Range {
                    start: c,
                    end:   c,
                }
            }
        )
    )
);

#[allow(dead_code)]
named!(literal<&[u8], Vec<char> >,
    map!(
        many1!(take_char),
        |cs| {
          cs
        }
    )
);

#[test]
fn issue_58() {
  let _ = range(&b"abcd"[..]);
  let _ = literal(&b"abcd"[..]);
}

//trace_macros!(false);

#[cfg(feature = "std")]
mod parse_int {
  use nom::HexDisplay;
  use nom::{digit, space, IResult};
  use std::str;

  named!(parse_ints<Vec<i32>>, many0!(spaces_or_int));

  fn spaces_or_int(input: &[u8]) -> IResult<&[u8], i32> {
    println!("{}", input.to_hex(8));
    do_parse!(
      input,
      opt!(complete!(space)) >> res: map!(complete!(digit), |x| {
        println!("x: {:?}", x);
        let result = str::from_utf8(x).unwrap();
        println!("Result: {}", result);
        println!("int is empty?: {}", x.is_empty());
        match result.parse() {
          Ok(i) => i,
          Err(e) => panic!("UH OH! NOT A DIGIT! {:?}", e),
        }
      }) >> (res)
    )
  }

  #[test]
  fn issue_142() {
    let subject = parse_ints(&b"12 34 5689a"[..]);
    let expected = Ok((&b"a"[..], vec![12, 34, 5689]));
    assert_eq!(subject, expected);

    let subject = parse_ints(&b"12 34 5689 "[..]);
    let expected = Ok((&b" "[..], vec![12, 34, 5689]));
    assert_eq!(subject, expected)
  }
}

#[test]
fn usize_length_bytes_issue() {
  use nom::be_u16;
  let _: IResult<&[u8], &[u8], u32> = length_bytes!(b"012346", be_u16);
}

/*
 DOES NOT COMPILE
#[test]
fn issue_152() {
  named!(take4, take!(4));
  named!(xyz, tag!("XYZ"));
  named!(abc, tag!("abc"));


  named!(sw,
    switch!(take4,
      b"abcd" => xyz |
      b"efgh" => abc
    )
  );
}
*/

#[test]
fn take_till_issue() {
  named!(nothing, take_till!(call!(|_| true)));

  assert_eq!(nothing(b""), Err(Err::Incomplete(Needed::Size(1))));
  assert_eq!(nothing(b"abc"), Ok((&b"abc"[..], &b""[..])));
}

named!(
  issue_498<Vec<&[u8]>>,
  separated_nonempty_list!(opt!(space), tag!("abcd"))
);

named!(issue_308(&str) -> bool,
    do_parse! (
        tag_s! ("foo") >>
        b: alt_complete! (
            map! (tag_s! ("1"), |_: &str|->bool {true}) |
            value! (false)
        ) >>
        (b) ));

#[cfg(feature = "alloc")]
fn issue_302(input: &[u8]) -> IResult<&[u8], Option<Vec<u64>>> {
  do_parse!(input, entries: cond!(true, count!(le_u64, 3)) >> (entries))
}

#[test]
fn issue_655() {
  use nom::{line_ending, not_line_ending};
  named!(twolines(&str) -> (&str, &str),
    do_parse!(
      l1 : not_line_ending >>
           line_ending >>
      l2 : not_line_ending >>
           line_ending >>
      ((l1, l2))
    )
  );

  assert_eq!(twolines("foo\nbar\n"), Ok(("", ("foo", "bar"))));
  assert_eq!(twolines("féo\nbar\n"), Ok(("", ("féo", "bar"))));
  assert_eq!(twolines("foé\nbar\n"), Ok(("", ("foé", "bar"))));
  assert_eq!(twolines("foé\r\nbar\n"), Ok(("", ("foé", "bar"))));
}

#[cfg(feature = "std")]
named!(issue_666 <CompleteByteSlice, CompleteByteSlice>, dbg_dmp!(tag!("abc")));

#[test]
fn issue_667() {
  use nom::alpha;

  named!(foo <CompleteByteSlice, Vec<CompleteByteSlice>>,
    many0!(
      alt!(alpha | is_a!("_"))
    )
  );
  assert_eq!(
    foo(CompleteByteSlice(b"")),
    Ok((CompleteByteSlice(b""), vec![]))
  );
  assert_eq!(
    foo(CompleteByteSlice(b"loremipsum")),
    Ok((
      CompleteByteSlice(b""),
      vec![CompleteByteSlice(b"loremipsum")]
    ))
  );
  assert_eq!(
    foo(CompleteByteSlice(b"lorem_ipsum")),
    Ok((
      CompleteByteSlice(b""),
      vec![
        CompleteByteSlice(b"lorem"),
        CompleteByteSlice(b"_"),
        CompleteByteSlice(b"ipsum"),
      ]
    ))
  );
  assert_eq!(
    foo(CompleteByteSlice(b"_lorem_ipsum")),
    Ok((
      CompleteByteSlice(b""),
      vec![
        CompleteByteSlice(b"_"),
        CompleteByteSlice(b"lorem"),
        CompleteByteSlice(b"_"),
        CompleteByteSlice(b"ipsum"),
      ]
    ))
  );
  assert_eq!(
    foo(CompleteByteSlice(b"!@#$")),
    Ok((CompleteByteSlice(b"!@#$"), vec![]))
  );
}

#[test]
fn issue_721() {
  assert_eq!(parse_to!("1234", u16), Ok(("", 1234)));
  assert_eq!(parse_to!("foo", String), Ok(("", "foo".to_string())));
}

#[cfg(feature = "alloc")]
named!(issue_717<&[u8], Vec<&[u8]> >,
  separated_list!(tag!([0x0]), is_not!([0x0u8]))
);

struct NoPartialEq {
  value: i32,
}

named!(issue_724<&str, i32>,
  do_parse!(
    metadata: permutation!(
      map!(tag!("hello"), |_| NoPartialEq { value: 1 }),
      map!(tag!("world"), |_| NoPartialEq { value: 2 })
    ) >>
    (metadata.0.value + metadata.1.value)
  )
);

named!(issue_741_str<CompleteStr, CompleteStr>, re_match!(r"^_?[A-Za-z][0-9A-Z_a-z-]*"));
named!(issue_741_bytes<CompleteByteSlice, CompleteByteSlice>, re_bytes_match!(r"^_?[A-Za-z][0-9A-Z_a-z-]*"));


#[test]
fn issue_752() {
    assert_eq!(
        Err::Error(nom::Context::Code("ab", nom::ErrorKind::ParseTo)),
        parse_to!("ab", usize).unwrap_err()
    )
}

fn atom_specials(c: u8) -> bool {
    c == b'q'
}

named!(
    capability<&str>,
    do_parse!(tag_s!(" ") >> _atom: map_res!(take_till1!(atom_specials), std::str::from_utf8) >> ("a"))
);

#[test]
fn issue_759() {
    assert_eq!(capability(b" abcqd"), Ok((&b"qd"[..], "a")));
}

named_args!(issue_771(count: usize)<Vec<u32>>,
  length_count!(value!(count), call!(nom::be_u32))
);

#[test]
fn issue_768() {
  named!(bit_vec8<CompleteByteSlice, Vec<u16>>, bits!(many0!(take_bits!(u16, 8))));
  named!(bit_vec4<CompleteByteSlice, Vec<u16>>, bits!(many0!(take_bits!(u16, 4))));
  named!(bit_vec3<CompleteByteSlice, Vec<u16>>, bits!(many0!(take_bits!(u16, 3))));
  named!(bit_vec11<CompleteByteSlice, Vec<u16>>, bits!(many0!(take_bits!(u16, 11))));

  let m: Vec<u8> = vec![70, 97, 106, 121, 86, 66, 105, 98, 86, 106, 101];
  assert_eq!(
    bit_vec8(CompleteByteSlice(m.as_slice())),
    Ok((CompleteByteSlice(&[]), vec![70, 97, 106, 121, 86, 66, 105, 98, 86, 106, 101]))
  );
  assert_eq!(
    bit_vec4(CompleteByteSlice(m.as_slice())),
    Ok((CompleteByteSlice(&[]), vec![4, 6, 6, 1, 6, 10, 7, 9, 5, 6, 4, 2, 6, 9, 6, 2, 5, 6, 6, 10, 6, 5]))
  );
  assert_eq!(
    bit_vec3(CompleteByteSlice(m.as_slice())),
    Ok((CompleteByteSlice(&[]), vec![2, 1, 4, 6, 0, 5, 5, 2, 3, 6, 2, 5, 3, 1, 0, 2, 3, 2, 2, 6, 1, 1, 2, 6, 3, 2, 4, 6, 2]))
  );
  assert_eq!(
    bit_vec11(CompleteByteSlice(m.as_slice())),
    Ok((CompleteByteSlice(&[]), vec![563, 90, 1266, 1380, 308, 1417, 717, 613]))
  );
}

/// This test is in a separate module to check that all required symbols are imported in
/// `escaped_transform!()`. Without the module, the `use`-es of the current module would
/// mask the error ('"Use of undeclared type or module `Needed`" in escaped_transform!').
mod issue_780 {
  named!(issue_780<&str, String>,
    escaped_transform!(call!(::nom::alpha), '\\', tag!("n"))
  );
}

// issue 617
named!(digits, take_while1!( is_digit ));
named!(multi_617<&[u8], () >, fold_many0!( digits, (), |_, _| {}));

// Sad :(
named!(multi_617_fails<&[u8], () >, fold_many0!( take_while1!( is_digit ), (), |_, _| {}));

mod issue_647 {
  use nom::{Err,be_f64};
  pub type Input<'a> = &'a [u8];

  #[derive(PartialEq, Debug, Clone)]
  struct Data {
      c: f64,
      v: Vec<f64>
  }

  fn list<'a,'b>(input: Input<'a>, _cs: &'b f64) -> Result<(Input<'a>,Vec<f64>), Err<&'a [u8]>> {
      separated_list_complete!(input, tag!(","),be_f64)
  }

  named!(data<Input,Data>, map!(
      do_parse!(
          c: be_f64 >>
          tag!("\n") >>
          v: call!(list,&c) >>
          (c,v)
      ), |(c,v)| {
          Data {
              c: c,
              v: v
          }
      }
  ));
}

named!(issue_775, take_till1!(|_| true));

#[test]
fn issue_848_overflow_incomplete_bits_to_bytes() {
  named!(parser<&[u8], &[u8]>, bits!(bytes!(take!(0x2000000000000000))));
  assert_eq!(parser(&b""[..]), Err(Err::Failure(error_position!(&b""[..], ErrorKind::TooLarge))));
}

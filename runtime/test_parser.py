"""Test the runtime.parser module."""

import unittest

import runtime.lexer
from runtime.parser import *

def token(value, kind):
    return lexer.TokenTuple(value=value, kind=kind)

asgn_token = token("=", lexer.OPERATOR)
asgnadd_token = token("+=", lexer.OPERATOR)
asgnsub_token = token("-=", lexer.OPERATOR)
asgnmul_token = token("*=", lexer.OPERATOR)
asgndiv_token = token("/=", lexer.OPERATOR)
asgnpow_token = token("^=", lexer.OPERATOR)
asgnmod_token = token("%=", lexer.OPERATOR)
plus_token = token("+", lexer.OPERATOR)
minus_token = token("-", lexer.OPERATOR)
neg_token = token("!", lexer.OPERATOR)
and_token = token("&&", lexer.OPERATOR)
or_token = token("||", lexer.OPERATOR)
xor_token = token("^|", lexer.OPERATOR)
equal_token = token("==", lexer.OPERATOR)
unequal_token = token("!=", lexer.OPERATOR)
smaller_token = token("<", lexer.OPERATOR)
larger_token = token(">", lexer.OPERATOR)
smequ_token = token("<=", lexer.OPERATOR)
lgequ_token = token(">=", lexer.OPERATOR)
mod_token = token("%", lexer.OPERATOR)
type_token = token(":", lexer.OPERATOR)
multiply_token = token("*", lexer.OPERATOR)
divide_token = token("/", lexer.OPERATOR)
power_token = token("^", lexer.OPERATOR)
lprt_token = token(")", lexer.LPRT)
sep_token = token(",", lexer.SEPARATOR)
identifier_token = token("abc", lexer.IDENTIFIER)
string_token = token("\"abc\"", lexer.STRING)
rprt_token = token("(", lexer.RPRT)
number_token = token("1", lexer.NUMBER)

operation_tokens = [plus_token, minus_token, sep_token, lprt_token, None]
value_tokens = [identifier_token, string_token, rprt_token, number_token]
all_tokens = operation_tokens + value_tokens

def clean_lex(expr):
    clean = lexer.run(expr)
    output = []
    for e in clean:
        if e.kind is not lexer.WHITESPACE:
            output.append(e)
    return output

class TestParser(unittest.TestCase):
    """Test the parser."""

    def test_is_assignment(self):
        cases = [
            (asgn_token, True),
            (asgnadd_token, True),
            (asgnsub_token, True),
            (asgnmul_token, True),
            (asgndiv_token, True),
            (asgnmod_token, True),
            (asgnpow_token, True),
            (None, False),
            (number_token, False),
        ]

        for tc in cases:
            self.assertEqual(is_assignment(tc[0]), tc[1],
                             "%s mistakingly reported as assignment" % str(tc[0]))

    def test_matching_block(self):
        cases = [
            (clean_lex("{}"), 1),
            (clean_lex("{"), -1),
            (clean_lex("}"), -1),
            (clean_lex("{{}"), -1),
            (clean_lex("{{}}"), 3),
            (clean_lex("{ 123; }"), 3),
        ]

        for tc in cases:
            self.assertEqual(find_matching_block(tc[0], 1), tc[1])


    def test_matching_prt(self):
        cases = [
            (clean_lex("()"), 1),
            (clean_lex("("), -1),
            (clean_lex(")"), -1),
            (clean_lex("(()"), -1),
            (clean_lex("(123)"), 2),
            (clean_lex("(12 12)"), 3),
        ]

        for tc in cases:
            self.assertEqual(find_matching_prt(tc[0], 1), tc[1])

    def test_arg_count(self):

        cases = [
            (plus_token, value_tokens, 2),
            (plus_token, operation_tokens, 1),
            (minus_token, value_tokens, 2),
            (minus_token, operation_tokens, 1),
            (neg_token, value_tokens, 1),
            (neg_token, operation_tokens, 1),
            (and_token, all_tokens, 2),
            (or_token, all_tokens, 2),
            (xor_token, all_tokens, 2),
            (equal_token, all_tokens, 2),
            (unequal_token, all_tokens, 2),
            (smaller_token, all_tokens, 2),
            (larger_token, all_tokens, 2),
            (smequ_token, all_tokens, 2),
            (lgequ_token, all_tokens, 2),
            (mod_token, all_tokens, 2),
            (type_token, all_tokens, 2),
            (multiply_token, all_tokens, 2),
            (divide_token, all_tokens, 2),
            (power_token, all_tokens, 2),
            (asgn_token, all_tokens, 2),
            (asgnadd_token, all_tokens, 2),
            (asgnsub_token, all_tokens, 2),
            (asgnmul_token, all_tokens, 2),
            (asgndiv_token, all_tokens, 2),
            (asgnpow_token, all_tokens, 2),
            (asgnmod_token, all_tokens, 2),
        ]

        for tc in cases:
            for e in tc[1]:
                self.assertEqual(get_arg_count(tc[0].value, e), tc[2],
                                 "bad operator arg count for %s when tested against %s" % (tc[0].value, e))

    def test_precedence(self):
        cases = [
            (neg_token, all_tokens, 7),
            (plus_token, operation_tokens, 7),
            (minus_token, operation_tokens, 7),
            (power_token, all_tokens, 6),
            (divide_token, all_tokens, 5),
            (multiply_token, all_tokens, 5),
            (plus_token, value_tokens, 4),
            (minus_token, value_tokens, 4),
            (type_token, all_tokens, 4),
            (mod_token, all_tokens, 3),
            (smaller_token, all_tokens, 2),
            (larger_token, all_tokens, 2),
            (smequ_token, all_tokens, 2),
            (lgequ_token, all_tokens, 2),
            (equal_token, all_tokens, 2),
            (unequal_token, all_tokens, 2),
            (and_token, all_tokens, 1),
            (or_token, all_tokens, 1),
            (xor_token, all_tokens, 1),
            (asgn_token, all_tokens, 0),
            (asgnadd_token, all_tokens, 0),
            (asgnsub_token, all_tokens, 0),
            (asgnmul_token, all_tokens, 0),
            (asgndiv_token, all_tokens, 0),
            (asgnpow_token, all_tokens, 0),
            (asgnmod_token, all_tokens, 0),
        ]

        for tc in cases:
            for e in tc[1]:
                self.assertEqual(get_precedence(tc[0].value, e), tc[2],
                                 "bad operator precedence for %s when tested against %s" % (tc[0].value, e))

    def test_associativity(self):
        cases = [
            (neg_token, all_tokens, False),
            (plus_token, operation_tokens, False),
            (minus_token, operation_tokens, False),
            (power_token, all_tokens, False),
            (divide_token, all_tokens, True),
            (multiply_token, all_tokens, True),
            (plus_token, value_tokens, True),
            (minus_token, value_tokens, True),
            (type_token, all_tokens, True),
            (mod_token, all_tokens, True),
            (smaller_token, all_tokens, True),
            (larger_token, all_tokens, True),
            (smequ_token, all_tokens, True),
            (lgequ_token, all_tokens, True),
            (equal_token, all_tokens, True),
            (unequal_token, all_tokens, True),
            (and_token, all_tokens, True),
            (or_token, all_tokens, True),
            (xor_token, all_tokens, True),
            (asgn_token, all_tokens, True),
            (asgnadd_token, all_tokens, True),
            (asgnsub_token, all_tokens, True),
            (asgnmul_token, all_tokens, True),
            (asgndiv_token, all_tokens, True),
            (asgnpow_token, all_tokens, True),
            (asgnmod_token, all_tokens, True),
        ]

        for tc in cases:
            for e in tc[1]:
                self.assertEqual(is_left_associative(tc[0].value, e), tc[2],
                                 "bad operator associativity for %s when tested against %s" % (tc[0].value, e))


    def test_expression(self):
        pass

    def test_declaration(self):
        pass

    def test_assignment(self):
        pass

    def test_function(self):
        pass

    def test_if(self):
        pass

    def test_for(self):
        pass

    def test_while(self):
        pass

    def test_sequence(self):
        pass

    def test_optimize(self):
        pass

    def test_generate(self):
        pass


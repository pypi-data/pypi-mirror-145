from colassigner.util import camel_to_snake


def test_cc_to_snake():
    s = "ClassToBeRenamed"
    s2 = "ClassWithAOneLetterWord"
    s3 = "ClassWith1Number"
    s4 = "ClassWith10Number"

    assert camel_to_snake(s) == "class_to_be_renamed"
    assert camel_to_snake(s2) == "class_with_a_one_letter_word"
    assert camel_to_snake(s3) == "class_with_1_number"
    assert camel_to_snake(s4) == "class_with_10_number"

from . import comparison_levels_library as cl


def exact_match(
    col_name,
    term_frequency_adjustments=False,
    m_probability_exact_match=0.9,
    m_probability_else=0.1,
):
    return {
        "comparison_levels": [
            cl.null_level(col_name),
            cl.exact_match_level(
                col_name,
                term_frequency_adjustments=term_frequency_adjustments,
                m_probability=m_probability_exact_match,
            ),
            cl.else_level(m_probability=m_probability_else),
        ]
    }


def levenshtein(
    col_name,
    distance_threshold=2,
    term_frequency_adjustments=False,
    m_probability_exact_match=0.7,
    m_probability_leven=0.2,
    m_probability_else=0.1,
):
    return {
        "comparison_levels": [
            cl.null_level(col_name),
            cl.exact_match_level(
                col_name,
                term_frequency_adjustments=term_frequency_adjustments,
                m_probability=m_probability_exact_match,
            ),
            cl.levenshtein_level(
                col_name,
                distance_threshold=distance_threshold,
                m_probability=m_probability_leven,
            ),
            cl.else_level(m_probability=m_probability_else),
        ]
    }

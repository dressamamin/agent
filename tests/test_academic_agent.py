"""Unit tests for AcademicWritingAgent."""

import pytest

from agent.academic_agent import AcademicWritingAgent, CitationInfo


@pytest.fixture
def agent() -> AcademicWritingAgent:
    return AcademicWritingAgent()


# ---------------------------------------------------------------------------
# Paper structure
# ---------------------------------------------------------------------------

class TestGetPaperStructure:
    def test_research_paper_has_expected_sections(self, agent):
        sections = agent.get_paper_structure("research")
        assert "Abstract" in sections
        assert "Introduction" in sections
        assert "Methodology" in sections
        assert "Results" in sections
        assert "Discussion" in sections
        assert "Conclusion" in sections
        assert "References" in sections

    def test_thesis_has_title_page(self, agent):
        sections = agent.get_paper_structure("thesis")
        assert "Title Page" in sections

    def test_review_paper_has_synthesis(self, agent):
        sections = agent.get_paper_structure("review")
        assert any("Synthesis" in s for s in sections)

    def test_conference_paper(self, agent):
        sections = agent.get_paper_structure("conference")
        assert "Abstract" in sections
        assert "References" in sections

    def test_case_study_paper(self, agent):
        sections = agent.get_paper_structure("case_study")
        assert "Case Description" in sections

    def test_invalid_type_raises_value_error(self, agent):
        with pytest.raises(ValueError, match="Unknown paper type"):
            agent.get_paper_structure("nonexistent_type")

    def test_case_insensitive_input(self, agent):
        sections = agent.get_paper_structure("Research")
        assert len(sections) > 0

    def test_describe_paper_structure_returns_string(self, agent):
        result = agent.describe_paper_structure("research")
        assert isinstance(result, str)
        assert "Research" in result


# ---------------------------------------------------------------------------
# Section guides
# ---------------------------------------------------------------------------

class TestSectionGuides:
    @pytest.mark.parametrize("section", [
        "abstract", "introduction", "literature_review",
        "methodology", "results", "discussion", "conclusion", "references",
    ])
    def test_known_section_returns_guide(self, agent, section):
        guide = agent.get_section_guide(section)
        assert guide.name
        assert guide.purpose
        assert len(guide.key_elements) > 0
        assert len(guide.tips) > 0
        assert guide.word_count_guide

    def test_unknown_section_raises_value_error(self, agent):
        with pytest.raises(ValueError, match="Unknown section"):
            agent.get_section_guide("banana")

    def test_describe_section_contains_key_headings(self, agent):
        text = agent.describe_section("introduction")
        assert "PURPOSE" in text
        assert "KEY ELEMENTS" in text
        assert "WRITING TIPS" in text
        assert "TYPICAL LENGTH" in text

    def test_section_name_case_insensitive(self, agent):
        guide = agent.get_section_guide("Introduction")
        assert guide.name == "Introduction"


# ---------------------------------------------------------------------------
# Abstract template
# ---------------------------------------------------------------------------

class TestAbstractTemplate:
    def test_template_is_non_empty_string(self, agent):
        template = agent.get_abstract_template()
        assert isinstance(template, str)
        assert len(template) > 50

    def test_template_mentions_keywords(self, agent):
        template = agent.get_abstract_template()
        assert "Keywords" in template

    def test_template_has_methodology_placeholder(self, agent):
        template = agent.get_abstract_template()
        assert "Methodology" in template


# ---------------------------------------------------------------------------
# Citation formatting — APA
# ---------------------------------------------------------------------------

class TestCitationAPA:
    def _journal_info(self) -> CitationInfo:
        return CitationInfo(
            authors=["Jane Smith", "John Doe"],
            year=2023,
            title="Effects of climate change on biodiversity",
            journal="Nature",
            volume="612",
            issue="3",
            pages="100-115",
            doi="10.1000/xyz123",
        )

    def test_apa_journal_contains_authors(self, agent):
        citation = agent.format_citation(self._journal_info(), style="apa")
        assert "Smith" in citation
        assert "Doe" in citation

    def test_apa_journal_contains_year(self, agent):
        citation = agent.format_citation(self._journal_info(), style="apa")
        assert "2023" in citation

    def test_apa_journal_contains_doi(self, agent):
        citation = agent.format_citation(self._journal_info(), style="apa")
        assert "10.1000/xyz123" in citation

    def test_apa_single_author(self, agent):
        info = CitationInfo(
            authors=["Alice Brown"],
            year=2021,
            title="A single author study",
            journal="Science",
            volume="10",
        )
        citation = agent.format_citation(info, style="apa")
        assert "Brown, A." in citation

    def test_apa_three_or_more_authors(self, agent):
        info = CitationInfo(
            authors=["Alpha One", "Beta Two", "Gamma Three"],
            year=2020,
            title="Multi-author work",
            journal="Cell",
        )
        citation = agent.format_citation(info, style="apa")
        assert "One" in citation
        assert "&" in citation

    def test_apa_book(self, agent):
        info = CitationInfo(
            authors=["Robert Johnson"],
            year=2019,
            title="Research Methods",
            publisher="Academic Press",
            city="London",
            edition="3rd",
        )
        citation = agent.format_citation(info, style="apa")
        assert "Johnson" in citation
        assert "Academic Press" in citation
        assert "3rd" in citation

    def test_apa_invalid_style_raises(self, agent):
        with pytest.raises(ValueError, match="Unknown citation style"):
            agent.format_citation(self._journal_info(), style="harvard")


# ---------------------------------------------------------------------------
# Citation formatting — MLA
# ---------------------------------------------------------------------------

class TestCitationMLA:
    def test_mla_journal_format(self, agent):
        info = CitationInfo(
            authors=["Jane Smith"],
            year=2023,
            title="An MLA title",
            journal="PMLA",
            volume="138",
            issue="2",
            pages="200-220",
        )
        citation = agent.format_citation(info, style="mla")
        assert "Smith, Jane" in citation
        assert '"An MLA title."' in citation
        assert "*PMLA*" in citation

    def test_mla_two_authors(self, agent):
        info = CitationInfo(
            authors=["Jane Smith", "Mark Brown"],
            year=2023,
            title="Collaborative work",
            journal="PMLA",
        )
        citation = agent.format_citation(info, style="mla")
        assert "et al." not in citation
        assert "and" in citation

    def test_mla_three_or_more_uses_et_al(self, agent):
        info = CitationInfo(
            authors=["Jane Smith", "Mark Brown", "Lucy Green"],
            year=2023,
            title="Group work",
            journal="PMLA",
        )
        citation = agent.format_citation(info, style="mla")
        assert "et al." in citation


# ---------------------------------------------------------------------------
# Citation formatting — Chicago
# ---------------------------------------------------------------------------

class TestCitationChicago:
    def test_chicago_journal_format(self, agent):
        info = CitationInfo(
            authors=["David Lee"],
            year=2022,
            title="Chicago citation test",
            journal="American Historical Review",
            volume="127",
            issue="1",
            pages="50-75",
        )
        citation = agent.format_citation(info, style="chicago")
        assert "Lee" in citation
        assert "2022" in citation
        assert "*American Historical Review*" in citation

    def test_chicago_book_format(self, agent):
        info = CitationInfo(
            authors=["Susan Park"],
            year=2018,
            title="Historical Analysis",
            publisher="University of Chicago Press",
            city="Chicago",
        )
        citation = agent.format_citation(info, style="chicago")
        assert "Park" in citation
        assert "University of Chicago Press" in citation


# ---------------------------------------------------------------------------
# In-text citations
# ---------------------------------------------------------------------------

class TestInTextCitation:
    def test_apa_single_author(self, agent):
        result = agent.in_text_citation(["Jane Smith"], 2021, style="apa")
        assert result == "(Smith, 2021)"

    def test_apa_two_authors(self, agent):
        result = agent.in_text_citation(["Jane Smith", "John Doe"], 2021, style="apa")
        assert "Smith" in result
        assert "Doe" in result
        assert "&" in result

    def test_apa_three_plus_uses_et_al(self, agent):
        result = agent.in_text_citation(
            ["Jane Smith", "John Doe", "Mary Jones"], 2021, style="apa"
        )
        assert "et al." in result

    def test_apa_with_page(self, agent):
        result = agent.in_text_citation(["Jane Smith"], 2021, style="apa", page="45")
        assert "p. 45" in result

    def test_mla_no_year(self, agent):
        result = agent.in_text_citation(["Jane Smith"], 2021, style="mla", page="30")
        assert "2021" not in result
        assert "Smith" in result
        assert "30" in result

    def test_invalid_style_raises(self, agent):
        with pytest.raises(ValueError, match="Unknown citation style"):
            agent.in_text_citation(["Jane Smith"], 2021, style="oxford")


# ---------------------------------------------------------------------------
# Writing analysis
# ---------------------------------------------------------------------------

class TestWritingAnalysis:
    def test_detects_contractions(self, agent):
        issues = agent.analyse_writing("We don't have enough data.")
        categories = [i["category"] for i in issues]
        assert "Formality" in categories

    def test_detects_first_person_hedging(self, agent):
        issues = agent.analyse_writing("I think the results show a trend.")
        categories = [i["category"] for i in issues]
        assert "Academic voice" in categories

    def test_detects_vague_words(self, agent):
        issues = agent.analyse_writing("There are a lot of things to consider.")
        matches = [i["match"].lower() for i in issues]
        assert "a lot" in matches or any("thing" in m for m in matches)

    def test_clean_text_returns_empty_list(self, agent):
        clean_text = (
            "The results demonstrate a statistically significant relationship "
            "between the variables."
        )
        issues = agent.analyse_writing(clean_text)
        assert issues == []

    def test_describe_writing_analysis_no_issues(self, agent):
        result = agent.describe_writing_analysis(
            "The study demonstrates significant outcomes."
        )
        assert "No common issues" in result

    def test_describe_writing_analysis_with_issues(self, agent):
        result = agent.describe_writing_analysis("I think things are very clear.")
        assert "potential issue" in result
        assert "Suggestion" in result

    def test_issues_sorted_by_position(self, agent):
        text = "I think we don't have a lot of things."
        issues = agent.analyse_writing(text)
        positions = [i["position"] for i in issues]
        assert positions == sorted(positions)


# ---------------------------------------------------------------------------
# Literature review tips
# ---------------------------------------------------------------------------

class TestLiteratureReviewTips:
    def test_returns_non_empty_string(self, agent):
        tips = agent.get_literature_review_tips()
        assert isinstance(tips, str) and len(tips) > 100

    def test_contains_key_steps(self, agent):
        tips = agent.get_literature_review_tips()
        assert "STEP 1" in tips
        assert "STEP 5" in tips
        assert "CRITICAL EVALUATION" in tips


# ---------------------------------------------------------------------------
# Research question guide
# ---------------------------------------------------------------------------

class TestResearchQuestionGuide:
    def test_returns_non_empty_string(self, agent):
        guide = agent.get_research_question_guide()
        assert isinstance(guide, str) and len(guide) > 100

    def test_contains_pico_framework(self, agent):
        guide = agent.get_research_question_guide()
        assert "PICO" in guide


# ---------------------------------------------------------------------------
# Help
# ---------------------------------------------------------------------------

class TestHelp:
    def test_help_returns_string(self, agent):
        h = agent.help()
        assert isinstance(h, str)
        assert "CAPABILITIES" in h

    def test_help_lists_all_paper_types(self, agent):
        h = agent.help()
        for pt in agent.PAPER_TYPES:
            assert pt in h

    def test_help_lists_all_sections(self, agent):
        h = agent.help()
        for sec in agent.SECTIONS:
            assert sec in h

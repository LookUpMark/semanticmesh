"""Unit tests for web_search_fallback — UT-18"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.generation.answer_generator import web_search_fallback

_TAVILY = "langchain_community.tools.tavily_search.TavilySearchResults"
_DDG = "langchain_community.tools.DuckDuckGoSearchRun"


class TestWebSearchFallback:
    def test_returns_web_search_prefix(self) -> None:
        with patch(_TAVILY) as mock_tavily:
            mock_tool = MagicMock()
            mock_tool.invoke.return_value = [{"content": "some result"}]
            mock_tavily.return_value = mock_tool
            result = web_search_fallback("Who is a customer?")
        assert result.startswith("[Source: Web Search]")

    def test_tavily_result_included_in_output(self) -> None:
        with patch(_TAVILY) as mock_tavily:
            mock_tool = MagicMock()
            mock_tool.invoke.return_value = [{"content": "Tavily says hello"}]
            mock_tavily.return_value = mock_tool
            result = web_search_fallback("test")
        assert "Tavily says hello" in result

    def test_duckduckgo_fallback_when_tavily_import_error(self) -> None:
        with patch(_TAVILY, side_effect=ImportError), patch(_DDG) as mock_ddg:
            mock_tool = MagicMock()
            mock_tool.run.return_value = "DDG result"
            mock_ddg.return_value = mock_tool
            result = web_search_fallback("test query")
        assert "[Source: Web Search]" in result
        assert "DDG result" in result

    def test_duckduckgo_fallback_when_tavily_raises(self) -> None:
        with patch(_TAVILY) as mock_tavily:
            mock_tool = MagicMock()
            mock_tool.invoke.side_effect = RuntimeError("API error")
            mock_tavily.return_value = mock_tool
            with patch(_DDG) as mock_ddg:
                mock_tool2 = MagicMock()
                mock_tool2.run.return_value = "fallback result"
                mock_ddg.return_value = mock_tool2
                result = web_search_fallback("query")
        assert "fallback result" in result

    def test_all_search_fails_returns_graceful_message(self) -> None:
        with patch(_TAVILY, side_effect=ImportError), patch(_DDG, side_effect=ImportError):
            result = web_search_fallback("unknown query")
        assert "[Source: Web Search]" in result
        assert "No external results" in result

    def test_empty_tavily_result_falls_through_to_ddg(self) -> None:
        with patch(_TAVILY) as mock_tavily:
            mock_tool = MagicMock()
            mock_tool.invoke.return_value = []  # empty → falls through
            mock_tavily.return_value = mock_tool
            with patch(_DDG) as mock_ddg:
                mock_tool2 = MagicMock()
                mock_tool2.run.return_value = "DDG content"
                mock_ddg.return_value = mock_tool2
                result = web_search_fallback("query")
        assert "DDG content" in result


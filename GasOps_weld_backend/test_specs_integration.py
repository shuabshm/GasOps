"""
Test script to verify the Specifications feature integration

This script tests:
1. Supervisor routing to SpecsAgent
2. SpecsAgent functionality
3. Specs LLM search and answer generation
4. End-to-end integration
"""

import asyncio
import logging
from supervisor.supervisor import supervisor
from agents.specs_agent import handle_specs_agent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def test_supervisor_routing():
    """Test that supervisor correctly routes specs questions to SpecsAgent"""
    print("\n" + "="*80)
    print("TEST 1: Supervisor Routing to SpecsAgent")
    print("="*80)

    test_questions = [
        "What welding requirements apply to gas pipelines?",
        "What's required before a welder can weld on Company-owned piping?",
        "What are the inspection procedures for pipeline welding?",
        "What specifications are needed for pipeline materials?",
        "Show me work orders in Bronx",  # Should route to WeldInsightsAgent
        "What's the weather today?",  # Should answer directly
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            result = await supervisor(question, database_name="test_db", auth_token="test_token")

            if isinstance(result, dict):
                if "answer" in result and "sources" in result:
                    print(f"✓ Routed to SpecsAgent")
                    print(f"  Answer preview: {result['answer'][:100]}...")
                    print(f"  Sources: {len(result.get('sources', []))} documents")
                elif "answer" in result:
                    print(f"✓ Direct answer (no agent): {result['answer'][:100]}...")
                else:
                    print(f"✓ Routed to other agent")
            else:
                print(f"✗ Unexpected response format: {type(result)}")

        except Exception as e:
            print(f"✗ Error: {e}")

        print("-" * 50)


def test_specs_agent_directly():
    """Test SpecsAgent directly without supervisor"""
    print("\n" + "="*80)
    print("TEST 2: SpecsAgent Direct Testing")
    print("="*80)

    test_questions = [
        "What's required before a welder can weld on Company-owned piping?",
        "What are the welding requirements for gas pipelines?",
    ]

    for question in test_questions:
        print(f"\nQuestion: {question}")
        try:
            result = handle_specs_agent(question)

            print(f"✓ Answer received")
            print(f"  Answer: {result['answer'][:200]}...")

            if result.get('sources'):
                print(f"\n  Sources ({len(result['sources'])}):")
                for i, source in enumerate(result['sources'][:3], 1):
                    print(f"    {i}. {source['document']} (chunk {source['chunk']}, page {source['page']}, score: {source['score']:.2f})")
            else:
                print("  No sources found")

        except Exception as e:
            print(f"✗ Error: {e}")
            import traceback
            traceback.print_exc()

        print("-" * 50)


def test_specs_llm():
    """Test specs_llm module directly"""
    print("\n" + "="*80)
    print("TEST 3: Specs LLM Module Testing")
    print("="*80)

    try:
        from tools.specs_llm import ask_question

        question = "What welding requirements apply to gas pipelines?"
        print(f"Question: {question}\n")

        result = ask_question(question, top_k=3)

        print(f"✓ Search and answer generation successful")
        print(f"\nAnswer:\n{result['answer']}")

        if result.get('sources'):
            print(f"\nSources ({len(result['sources'])}):")
            for i, source in enumerate(result['sources'], 1):
                print(f"  {i}. {source['document']} (chunk {source['chunk']}, page {source['page']}, relevance: {source['score']:.2f})")
        else:
            print("\n⚠ No sources found - Index may not be populated yet")
            print("  Run tools/specs_extraction.py followed by tools/index_vectorize_specs.py to populate the index")

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()


def check_prerequisites():
    """Check if all prerequisites are met"""
    print("\n" + "="*80)
    print("PREREQUISITE CHECK")
    print("="*80)

    import os
    from pathlib import Path

    checks = {
        "specs folder exists": Path("specs").exists(),
        "specs_extracted_texts folder exists": Path("specs_extracted_texts").exists(),
        "specs_extraction.py exists": Path("tools/specs_extraction.py").exists(),
        "index_vectorize_specs.py exists": Path("tools/index_vectorize_specs.py").exists(),
        "specs_llm.py exists": Path("tools/specs_llm.py").exists(),
        "specs_agent.py exists": Path("agents/specs_agent.py").exists(),
        "AZURE_SEARCH_ENDPOINT set": bool(os.getenv("AZURE_SEARCH_ENDPOINT")),
        "AZURE_SEARCH_KEY set": bool(os.getenv("AZURE_SEARCH_KEY")),
        "AZURE_OPENAI_ENDPOINT set": bool(os.getenv("AZURE_OPENAI_ENDPOINT")),
        "AZURE_OPENAI_API_KEY set": bool(os.getenv("AZURE_OPENAI_API_KEY")),
    }

    all_passed = True
    for check, passed in checks.items():
        status = "✓" if passed else "✗"
        print(f"{status} {check}")
        if not passed:
            all_passed = False

    if not all_passed:
        print("\n⚠ Some prerequisites are missing. Please fix before running tests.")
    else:
        print("\n✓ All prerequisites met!")

    return all_passed


async def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("GasOps Weld Backend - Specifications Feature Integration Tests")
    print("="*80)

    # Check prerequisites first
    if not check_prerequisites():
        print("\nSkipping tests due to missing prerequisites.")
        return

    # Test supervisor routing
    await test_supervisor_routing()

    # Test specs agent directly
    test_specs_agent_directly()

    # Test specs LLM module
    test_specs_llm()

    print("\n" + "="*80)
    print("TESTS COMPLETED")
    print("="*80)
    print("\nNext steps:")
    print("1. If index not populated: Run tools/specs_extraction.py")
    print("2. Then run: python tools/index_vectorize_specs.py")
    print("3. Test via API: POST to /ask with specs-related questions")
    print("="*80)


if __name__ == "__main__":
    asyncio.run(main())

import argparse


def run():
    try:
        from langchain_core.output_parsers import StrOutputParser
        from langchain_core.prompts import PromptTemplate
        from langchain_core.runnables import RunnableLambda
    except ImportError:
        print("SMOKE_SKIPPED install requirements.txt (langchain-core required)")
        return None
    prompt = PromptTemplate.from_template("Rewrite as a concise title: {text}")
    demo_model = RunnableLambda(lambda rendered: "Demo output: " + rendered.to_string())
    chain = prompt | demo_model | StrOutputParser()
    result = chain.invoke({"text": "A guide to storing and finding text vectors"})
    print(result)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--smoke", action="store_true")
    args = parser.parse_args()
    result = run()
    if result is not None and args.smoke:
        assert result.startswith("Demo output:")
        print("SMOKE_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

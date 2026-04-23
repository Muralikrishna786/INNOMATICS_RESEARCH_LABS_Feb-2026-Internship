from workflow import build_graph

def main():
    app = build_graph()

    print("🤖 RAG Customer Support Bot (type 'exit' to quit)\n")

    while True:
        query = input("You: ")

        if query.lower() == "exit":
            break

        try:
            result = app.invoke({"query": query})
            DEBUG = False
            if DEBUG:
                print("DEBUG RESULT:", result) 
            
            if not result or not isinstance(result, dict):
                print("\nBot: ⚠️ Invalid response from the system.")
                continue

            response = result.get("response", "").strip()

            if response:
                print("\nBot:", response)
            else:
                print("\nBot: ⚠️ No response generated.")

        except Exception as e:
            print("\n⚠️ Error occurred:", str(e))

        print("-" * 50)

if __name__ == "__main__":
    main()
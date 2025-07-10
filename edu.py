import os
import re
import time
from typing import Optional, List
from llama_cpp import Llama


class HybridInstantEduGPT:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.llm = None
        self.current_mode = "edu"
        self.last_instant_answer = None
        self.load_model()

        self.instant_patterns = {
            "edu": {
                r"\b(what is|define|explain).*\b(artificial intelligence|AI)\b":
                    "Artificial Intelligence (AI) is the simulation of human-like intelligence in machines. It includes learning, reasoning, and self-correction. AI applications include robotics, language translation, image recognition, and expert systems.",

                r"\b(what is|define|explain).*\b(machine learning|ML)\b":
                    "Machine Learning (ML) is a subset of AI focused on algorithms that allow systems to learn from data and make predictions or decisions without being explicitly programmed. Common ML techniques include supervised, unsupervised, and reinforcement learning.",

                r"\b(what is|define|explain).*\b(operating system|OS|virtual memory|paging|deadlock)\b":
                    "An Operating System (OS) manages hardware resources and offers services to applications. Virtual memory allows systems to use disk storage as extra RAM. Paging divides memory into pages. Deadlock happens when processes are stuck waiting for each other's resources.",

                r"\b(what is|define|explain).*\b(database|DBMS|SQL|NoSQL|ACID)\b":
                    "A Database Management System (DBMS) helps create, manage, and interact with databases. SQL is used in relational databases (like MySQL), while NoSQL handles unstructured data (like MongoDB). ACID ensures transaction reliability: Atomicity, Consistency, Isolation, Durability.",
            },

            "interview": {
                r"\b(tell me about yourself( as a fresher)?( for software engineer(role)?)?)\b":
                    "I'm a computer science fresher with a strong grasp of programming in Python and Java. I’ve built several academic projects and participated in coding competitions. I’m eager to join a software engineering role to apply what I’ve learned and grow through hands-on experience.",

                r"\b(introduce yourself( as a fresher)?( for software engineer(role)?)?)\b":
                    "I’m a motivated computer science graduate with experience in building web and Python-based projects. I’m looking to begin my career as a software engineer where I can continue learning and contribute meaningfully to a tech team.",

                r"\b(why should we hire you|why hire you|what makes you unique)\b":
                    "I bring strong programming fundamentals, a problem-solving mindset, and eagerness to learn. I’ve worked on team projects, understand version control with Git, and can adapt quickly. I'm ready to contribute from day one.",
            }
        }

    def load_model(self):
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=450,
                n_threads=os.cpu_count(),
                use_mmap=True,
                use_mlock=False,
                n_gpu_layers=0,
                verbose=False
            )
            print("✅ Model loaded! Ready for LLM responses.")
        except Exception as e:
            print(f"❌ Model load failed: {e}")
            self.llm = None

    def set_mode(self, mode: str):
        if mode in ["edu", "interview"]:
            self.current_mode = mode
            print(f"🔄 Switched to {mode.capitalize()} Mode")

    def get_instant_response(self, user_input: str) -> Optional[str]:
        user_input = user_input.lower().strip()
        fallback_keywords = ["elaborate", "example", "sample", "explain more", "in detail"]

        patterns = self.instant_patterns.get(self.current_mode, {})

        for pattern, response in patterns.items():
            if re.search(pattern, user_input, re.IGNORECASE):
                self.last_instant_answer = response
                if any(keyword in user_input for keyword in fallback_keywords):
                    return None
                return f"⚡ INSTANT: {response}"

        return None

    def generate_llm_response(self, user_input: str) -> str:
        if not self.llm:
            return "🤖 I don’t have detailed info for that right now."

        try:
            # Build persona prompt based on mode
            if self.current_mode == "interview":
                base_prompt = (
                    "You are a final-year computer science student preparing for software engineering interviews. "
                    "Respond in 3 to 4 short, confident, non-academic sentences. Keep it crisp and relevant to a fresher profile.\n\n"
                )
            else:
                base_prompt = (
                    "You are a computer science teacher. "
                    "Answer the question in 3 to 4 short, clear sentences. Avoid going too deep into examples.\n\n"
                )

            if any(x in user_input.lower() for x in ["elaborate", "example", "sample", "in detail", "explain more"]):
                if self.last_instant_answer:
                    prompt = (
                        base_prompt +
                        f"Original Answer: {self.last_instant_answer}\n\nNow elaborate:\nAnswer:"
                    )
                else:
                    prompt = base_prompt + f"Question: {user_input}\nAnswer:"
            else:
                prompt = base_prompt + f"Question: {user_input}\nAnswer:"

            start_time = time.time()

            response = self.llm(
                prompt,
                max_tokens=120,
                temperature=0.2,
                top_p=0.8,
                top_k=40,
                repeat_penalty=1.05,
                stop=["User:", "Question:", "</s>"],
                echo=False
            )

            end_time = time.time()
            text = response["choices"][0]["text"].strip()

            if not text.endswith((".", "!", "?")):
                last_punc = max(text.rfind("."), text.rfind("!"), text.rfind("?"))
                if last_punc != -1:
                    text = text[:last_punc + 1]

            return f"🤖 {text}\n\n⏱️ {end_time - start_time:.2f}s"

        except Exception as e:
            return f"❌ Error: {str(e)}"

    def get_response(self, user_input: str) -> str:
        instant = self.get_instant_response(user_input)
        if instant:
            return instant
        return self.generate_llm_response(user_input)

    def get_examples(self) -> List[str]:
        if self.current_mode == "edu":
            return [
                "What is artificial intelligence?",
                "Explain virtual memory in OS",
                "What are ACID properties?",
                "TCP vs UDP differences",
                "What is binary search algorithm?"
            ]
        else:
            return [
                "Tell me about yourself",
                "Tell me about yourself as a fresher",
                "Why should we hire you?",
                "Introduce yourself for software engineer role",
            ]









import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import LlamaCpp
from langchain.chains import RetrievalQA




import re, traceback
from typing import List
from PyPDF2 import PdfReader



import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

from langchain.chains import RetrievalQA
from langchain_community.llms import LlamaCpp

class PDFQAHandler:
    def __init__(self):
        self.vectorstore = None
        self.qa = None

    def load_pdf(self, file_path):
        # Load PDF and split into chunks
        loader = PyPDFLoader(file_path)
        pages = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
        docs = splitter.split_documents(pages)

        # Create embeddings
        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={"device": "cpu"}
        )
        self.vectorstore = FAISS.from_documents(docs, embeddings)

        # Load the LLaMA model
        llm = LlamaCpp(
            model_path="models/llama-2-7b-chat.Q4_K_M.gguf",
            temperature=0.3,
            max_tokens=200,
            top_p=0.9,
            n_ctx=2048,
            verbose=False,
            n_threads=os.cpu_count(),
            n_batch=64
        )

        # Create QA chain
        self.qa = RetrievalQA.from_chain_type(
            llm=llm,
            retriever=self.vectorstore.as_retriever(),
            chain_type="stuff",
            return_source_documents=False
        )

    def answer_question(self, question):
            if not self.qa:
                return "Please upload a PDF first."
            result = self.qa.invoke({"query": question})
            answer = result.get("result", "No relevant answer found in the document.")

            # 🔥 Remove known hallucination prefixes repeatedly
            hallucination_prefixes = [
                "Unhelpful Answer:", "Helpful Answer:", "Answer:",
                "The topic of the document is", "The topic is",
                "Document discusses", "The subject of the document is"
            ]

            # Remove any known prefix from start (case insensitive)
            while True:
                trimmed = False
                for prefix in hallucination_prefixes:
                    if answer.lower().startswith(prefix.lower()):
                        answer = answer[len(prefix):].strip()
                        trimmed = True
                if not trimmed:
                    break

            # Also remove leading "The " or similar generalities if still vague
            if answer.lower().startswith("the ") and len(answer.split()) < 8:
                answer = "The answer may not be detailed enough. Please ask a more specific question."

            # Only return cleaned up single-line response (remove extra paragraphs)
            answer = answer.split("\n")[0].strip()

            return answer



# Singleton handler instance
_pdf_handler = PDFQAHandler()

def get_pdf_handler():
    return _pdf_handler




def main():
    model_path = "models/llama-2-7b-chat.Q4_K_M.gguf"
    print("🚀 Starting Hybrid Instant EduGPT...")
    print("💡 This version gives INSTANT responses for common questions!")

    try:
        bot = HybridInstantEduGPT(model_path)
        print("\n" + "="*60)
        print("⚡ Hybrid Instant EduGPT Ready!")
        print("="*60)
        print("🎯 INSTANT responses for common questions")
        print("🤖 LLM responses for complex queries")
        print("📝 Personalized responses using your information")
        print("\n📝 Commands: edu | interview | examples | context | exit")
        print("-"*60)

        while True:
            try:
                user_input = input(f"\n[{bot.current_mode.upper()}] 💬 You: ").strip()
                if user_input.lower() in ["exit", "quit", "q"]:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == "edu":
                    bot.set_mode("edu")
                    continue
                elif user_input.lower() == "interview":
                    bot.set_mode("interview")
                    continue
                elif user_input.lower() == "examples":
                    for i, example in enumerate(bot.get_examples(), 1):
                        print(f"   {i}. {example}")
                    continue
                elif user_input.lower() == "context":
                    bot.show_context()
                    continue
                elif not user_input:
                    continue

                print(f"\n{bot.get_response(user_input)}")

            except KeyboardInterrupt:
                print("\n\n👋 Goodbye!")
                break

    except Exception as e:
        print(f"❌ Error: {e}")




if __name__ == "__main__":
    main()
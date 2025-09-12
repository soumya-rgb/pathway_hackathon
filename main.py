# import pathway as pw
# from pathway.stdlib.indexing.nearest_neighbors import BruteForceKnnFactory
# from pathway.xpacks.llm import llms
# from pathway.xpacks.llm.document_store import DocumentStore
# from pathway.xpacks.llm.embedders import OpenAIEmbedder, GeminiEmbedder
# from pathway.xpacks.llm.parsers import UnstructuredParser, DoclingParser
# from pathway.xpacks.llm.splitters import TokenCountSplitter
# from pathway.xpacks.llm.mcp_server import McpServable, McpServer, PathwayMcp
# import warnings
# import asyncio
# import os 
# import json

# warnings.filterwarnings("ignore")


# class csv_schema(pw.Schema):
#     id: str
#     name: str
#     age: int
#     city: str

# def save_json(data, filename):
    
#     filepath = os.path.join("./output", filename)
#     try:
#         with open(filepath, "w", encoding="utf-8") as f:
#             json.dump(data, f, ensure_ascii=False, indent=2)
#         print(f"✅ Saved output to {filepath}")
#     except Exception as e:
#         print(f"⚠️ Error saving {filename}: {e}")

# async def parse_func():
#     try:
#         with open("./data/TSLA-Q3-2023-Update-3.pdf", "rb") as f:
#             pdf_data = f.read()
#             print(pdf_data[:20])  # Print first 20 bytes for verification
#             parser = DoclingParser(chunk=False)
#             doc = await parser.parse(pdf_data)
#             print(doc)
#             # save_json(doc, "parsed_docling.json")
#             return doc
#     except Exception as e:
#         print(f"Error in parse_func: {e}")
#         return None


# async def parse_pdf():
#     """Parse PDF using UnstructuredParser (no OpenGL dependency)"""
#     try:
#         parser = UnstructuredParser(
#             chunking_mode="by_title",
#             chunking_kwargs={
#                 "max_characters": 3000,
#                 "new_after_n_chars": 2000,
#             },
#         )
#         pdf_data = pw.io.fs.read(
#             path="./data/TSLA-Q3-2023-Update-3.pdf",
#             format="binary",
#             mode="static",
#             with_metadata=True,
#         )
#         # parsed_docs = parser.parse(pdf_data)
#         parsed_docs = pdf_data.with_columns(
#         parsed=parser(pdf_data.data)
#         )
#         print("PDF parsed successfully with UnstructuredParser")
#         print(parsed_docs)
#         # save_json(parsed_docs, "parsed_unstructured.json")
#         return parsed_docs

#     except Exception as e:
#         print(f"Error parsing PDF: {e}")
#         return None
    
# if __name__ == "__main__":
#     csv_data = pw.io.fs.read(
#         path="./test.csv", format="csv", schema=csv_schema, mode="static"
#     )

#     pw.io.fs.write(table=csv_data, filename="./csv_out1.txt", format="csv")

#     text_splitter = TokenCountSplitter(
#         min_tokens=100, max_tokens=500, encoding_name="cl100k_base"
#     )

#     embedder = GeminiEmbedder(
#         model="gemini-embedding-001",
#         api_key="AIzaSyDa8iYfjwMLOXT0AzgkYwi9niA67Qun0JY",
#     )

#     retriever_factory = BruteForceKnnFactory(
#         embedder=embedder,
#     )

#     parser = UnstructuredParser(
#         chunking_mode="by_title",
#         chunking_kwargs={
#             "max_characters": 3000,
#             "new_after_n_chars": 2000,
#         },
#     )

#     asyncio.run(parse_func())
#     asyncio.run(parse_pdf())

#     pw.run()
#     print("done")

import logging

import pathway as pw
from dotenv import load_dotenv
from pathway.xpacks.llm.question_answering import SummaryQuestionAnswerer
from pathway.xpacks.llm.servers import QASummaryRestServer
from pydantic import BaseModel, ConfigDict, InstanceOf

# To use advanced features with Pathway Scale, get your free license key from
# https://pathway.com/features and paste it below.
# To use Pathway Community, comment out the line below.
# pw.set_license_key("demo-license-key-with-telemetry")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()


class App(BaseModel):
    question_answerer: InstanceOf[SummaryQuestionAnswerer]
    host: str = "0.0.0.0"
    port: int = 8000

    with_cache: bool = True
    terminate_on_error: bool = False

    def run(self) -> None:
        server = QASummaryRestServer(self.host, self.port, self.question_answerer)
        server.run(
            with_cache=self.with_cache,
            terminate_on_error=self.terminate_on_error,
        )

    model_config = ConfigDict(extra="forbid")


if __name__ == "__main__":
    with open("app.yaml") as f:
        config = pw.load_yaml(f)
    app = App(**config)
    app.run()

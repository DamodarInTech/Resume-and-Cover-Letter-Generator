import chromadb
import uuid
import json

# Initialize Persistent ChromaDB Client
# This will create or use a local folder "chroma_storage"
chroma_client = chromadb.PersistentClient(path="chroma_storage")

def save_to_chromadb(collection_name, data, unique_id=None):
    """
    Save data (a dict) to a ChromaDB collection.
    """
    try:
        collection = chroma_client.get_or_create_collection(name=collection_name)
        document_id = unique_id or str(uuid.uuid4())

        # Convert Python dict to a valid JSON string
        json_data = json.dumps(data, ensure_ascii=False)

        # Add the JSON string as a document to Chroma
        collection.add(
            documents=[json_data],
            metadatas=[{"source": collection_name}],
            ids=[document_id],
        )
        print(f"Data saved to ChromaDB collection '{collection_name}' with ID '{document_id}'")

    except Exception as e:
        raise ValueError(f"Error saving data to ChromaDB: {e}")

def fetch_from_chromadb(collection_name):
    """
    Fetch all data from a ChromaDB collection.
    Returns a dictionary with "documents" (list) and "metadatas" (list).
    The 'documents' list items are Python dictionaries (after JSON-deserialization).
    """
    try:
        collection = chroma_client.get_or_create_collection(name=collection_name)
        results = collection.get(include=["documents", "metadatas"])

        parsed_documents = []
        for doc_str in results["documents"]:
            # Attempt to parse the doc string as JSON
            # If the LLM returned single quotes or invalid JSON, handle that fallback
            try:
                parsed_documents.append(json.loads(doc_str))
            except json.JSONDecodeError:
                # Attempt a naive single-quote replacement as a fallback
                temp_str = doc_str.replace("'", '"')
                try:
                    parsed_documents.append(json.loads(temp_str))
                except json.JSONDecodeError:
                    # If we still can't decode, store it as a raw string
                    parsed_documents.append({"raw_text": doc_str})

        # Replace raw strings with parsed dicts
        results["documents"] = parsed_documents
        return results

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format in ChromaDB data: {e}")
    except Exception as e:
        raise ValueError(f"Error fetching data from ChromaDB: {e}")

def reset_collection(collection_name):
    """
    Delete all data from a ChromaDB collection.
    Workaround for "Expected where to have exactly one operator, got {} in delete."
    """
    try:
        collection = chroma_client.get_or_create_collection(name=collection_name)
        # Instead of passing an empty where={}, pass ids of all docs
        docs = collection.get()
        if "ids" in docs and docs["ids"]:
            collection.delete(ids=docs["ids"])
        print(f"Cleared collection '{collection_name}'.")
    except Exception as e:
        raise ValueError(f"Error resetting ChromaDB collection: {e}")

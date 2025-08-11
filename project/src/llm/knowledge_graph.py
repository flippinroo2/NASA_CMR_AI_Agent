from neo4j import GraphDatabase
from sentence_transformers import SentenceTransformer


class KnowledgeGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            "bolt://localhost:7687", auth=("neo4j", "password")
        )
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def find_related_datasets(self, dataset_id: str, max_results: int = 5):
        """Find datasets related to a given dataset using knowledge graph"""
        with self.driver.session() as session:
            result = session.run(
                """
                MATCH (d1:Dataset {id: $dataset_id})-[:RELATED_TO*1..3]-(d2:Dataset)
                RETURN d2.id, d2.title, d2.description
                LIMIT $max_results
                """,
                dataset_id=dataset_id,
                max_results=max_results,
            )
            return [dict(record) for record in result]

    def semantic_search(self, query: str, max_results: int = 5):
        """Perform semantic search using embeddings"""
        query_embedding = self.embedding_model.encode(query)

        with self.driver.session() as session:
            result = session.run(
                """
                CALL db.index.vector.queryNodes('dataset_embeddings', $limit, $query_embedding)
                YIELD node, score
                RETURN node.id, node.title, node.description, score
                ORDER BY score DESC
                LIMIT $max_results
                """,
                query_embedding=list(query_embedding),
                max_results=max_results,
            )
            return [dict(record) for record in result]

    def build_relationships(self, datasets: list[dict]):
        """Build relationships between datasets in the knowledge graph"""
        with self.driver.session() as session:
            for dataset in datasets:
                # Create dataset node if it doesn't exist
                session.run(
                    """
                    MERGE (d:Dataset {id: $id})
                    SET d.title = $title,
                        d.description = $description,
                        d.embedding = $embedding
                    """,
                    id=dataset["id"],
                    title=dataset["title"],
                    description=dataset["description"],
                    embedding=list(self.embedding_model.encode(dataset["description"])),
                )

                # Create relationships based on shared attributes
                self._create_relationships(session, dataset)

    def _create_relationships(self, session, dataset: dict):
        """Create relationships based on dataset attributes"""
        with session:
            # Example: Create relationships based on instruments
            if "instruments" in dataset:
                for instrument in dataset["instruments"]:
                    session.run(
                        """
                      MATCH (d:Dataset {id: $dataset_id})
                      MERGE (i:Instrument {name: $instrument_name})
                      MERGE (d)-[:USES_INSTRUMENT]->(i)
                      """,
                        dataset_id=dataset["id"],
                        instrument_name=instrument,
                    )

            # Create relationships based on science keywords
            if "science_keywords" in dataset:
                for keyword in dataset["science_keywords"]:
                    session.run(
                        """
                      MATCH (d:Dataset {id: $dataset_id})
                      MERGE (k:Keyword {name: $keyword_name})
                      MERGE (d)-[:HAS_KEYWORD]->(k)
                      """,
                        dataset_id=dataset["id"],
                        keyword_name=keyword,
                    )

class Documents:
    def __init__(self, document, documents ):
        self.documents = documents
        self.document = document

    def get_relevant(self):
        relevant = []
        for i in self.documents:
            relevant.append(
                (i, sum([
                    self.documents[i][j] * self.document[j] for j in self.document
                ])
                )
            )
        relevant = sorted(relevant, key=lambda x: x[1], reverse=True)
        return relevant



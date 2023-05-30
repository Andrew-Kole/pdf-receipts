import pandas
from fpdf import FPDF

df = pandas.read_csv("articles.csv", dtype={"id":str})


class Article:

    def __init__(self, article_id):
        self.article_id = article_id
        self.article_name = df.loc[df["id"] == self.article_id, "name"].squeeze()
        self.price = df.loc[df["id"] == self.article_id, "price"].squeeze()

    def buy_article(self):
        """buying article"""
        df.loc[df["id"] == self.article_id, "in stock"] -= 1
        df.to_csv("articles.csv", index=False)

    def available(self):
        """check if article is available"""
        availability = df.loc[df["id"] == self.article_id, "in stock"].squeeze()
        if availability > 0:
            return True
        else:
            return False


class Receipt:

    def __init__(self, article_object):
        self.article_object = article_object

    def generate(self):
        """generate a receipt"""
        pdf = FPDF(orientation="P", unit="mm", format="A4")
        pdf.add_page()

        with open("number_rec.txt", "r") as file:
            number = file.read()

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Receipt nr.{number}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Article: {self.article_object.article_name.title()}", ln=1)

        pdf.set_font(family="Times", size=16, style="B")
        pdf.cell(w=50, h=8, txt=f"Price: {self.article_object.price}", ln=1)

        pdf.output(f"receipts/receipt{number}.pdf")

        number = int(number) + 1
        with open("number_rec.txt", "w") as file:
            file.write(str(number))


print(df)
id_article = input("Enter please the article id: ")
article = Article(id_article)

if article.available():
    article.buy_article()
    receipt = Receipt(article_object=article)
    receipt.generate()
else:
    print("This item is currently unavailable.")



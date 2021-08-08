from flask import Flask, render_template, request, jsonify
from  flask_cors import  CORS,cross_origin
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests


app = Flask(__name__)

#route to display the home page
@app.route('/',methods=['GET'])

@cross_origin()

def indexpage():
    return render_template('index.html')

# route to show the review comments
@app.route('/review', methods=['POST','GET'])

@cross_origin()

def review():
    if request.method == 'POST':
        try:
            searchString = request.form['content'].replace(' ', '')
            flipkart_url = "https://www.flipkart.com/search?q=" + searchString
            uClient = uReq(flipkart_url)
            flipkartPage = uClient.read()
            uClient.close()
            flipkart_html = bs(flipkartPage,"html.parser")
            bigboxes = flipkart_html.findAll("div",{"class":"_1AtVbE col-12-12"})
            del bigboxes[0:3]
            box = bigboxes[0]
            productLink = "https://www.flipkart.com" + box.div.div.div.a['href']
            prodResult = requests.get(productLink)
            prodResult.encoding = 'utf-8'
            product_html = bs(prodResult.text,"html.parser")
            commentboxes = product_html.find_all('div',{'class':'_16PBlm'})

            filename = searchString + '.csv'

            fw = open(filename,'w')
            headers = "Product Name, Customer Name, Rating, Heading, Comment \n"
            fw.write(headers)
            reviews = []
            for commentbox in commentboxes:
                try:
                    name = commentbox.div.div.find_all('p',{'_2sc7ZR _2V5EHH'})[0].text
                except:
                    name = 'No Name'

                try:
                    rating = commentbox.div.div.div.div.text
                except:
                    rating = 'No Rating'

                try:
                    commenthead = commenthead.div.div.div.p.text
                except:
                    commenthead = 'No Comment Heading'
                try:
                    commenttag = commentbox.div.div.find_all('div',{'class':''})
                    custmorComment = commenttag[0].div.text
                except Exception as e:
                    print('Exception: ',e)
                mydict = {"Product": searchString, "Name": name, "Rating": rating, "CommentHead": commenthead,
                          "Comment": custmorComment}
                reviews.append(mydict)
            return render_template('results.html', reviews = reviews[0:(len(reviews)-1)])
        except Exception as e:
            print('Exception: ',e)
            return 'something went wrong'
    else:
        return render_template('index.html')






if __name__ == '__main__':
    app.run(debug=True)



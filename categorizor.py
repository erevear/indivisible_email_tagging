import re
import csv
from bs4 import BeautifulSoup

class EmailCategorizor(object):
  def __init__(self, file_name):
    self.file_name = file_name

  def readEmails(self):
    #read in the emails from a csv and turn them to a list
    email_text_list = []
    with open(self.file_name) as csvDataFile:
      csvReader = csv.reader(csvDataFile)
      for row in csvReader:
        email_data = {}
        email_data["email"] = row[0]
        email_text_list.append(email_data)
    return email_text_list

  def cleanseText(self, text):
    #lowercase entire string of text and remove html, script and style tags
    soup = BeautifulSoup(text, 'lxml')
    for script in soup(["script", "style"]):
        script.extract()
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = text.replace('\n','')
    return text.lower()

  def classifyAction(self, text):
    #use regex to find certain phrases and words that associate text with a predefined action category
    #list of categories to apply
    categories = ["call", "text", "twitter", "donate",  "write", "petition","contact","email","volunteer","phone bank", "march"]
    script_tags = ""
    found_strings = ""
    output_row = []
    #dictionary of categories with the regex that will categorize them
    matchers = {"contact": r"((contact|reach out to|ask|tell) (your|\bthe\b|him|her|them|our))|(let (your|our) \w{0,10} know)","call":r"(call (your|\bthe\b|our))|\(\d{3}\) \d{3}-\d{4}|\d{3}-\d{3}-\d{4}|\(\d{3}\)-\d{3}-\d{4}|i am calling", "text":r"resistbot|\bcountable|sent a message to \w+", "write":r"(send|write) a (letter|postcard)|thank you note", "petition":r"sign \w{0,10} petition| petition", "twitter":r"tweet.*@\w{1,15}|tweet.*#\w{4,144}|retweet", "donate":r"donate|donations|donating|give \$\d{1,10}|contribute \$\d{1,10}", "email":r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+|email (your|\bthe\b)","phone bank":r"phone bank", "volunteer":r"volunteer opportunities", "march":r"(march|protest|rally) (for|against)"}
    for category in categories:
      searchObj = re.findall(matchers[category],text)
      if searchObj:
        script_tags += category + ", "
        found_strings += str(searchObj)
    output_row.append(script_tags)
    output_row.append(found_strings)
    return output_row


  def classifySubject(self, text):
    #use regex to find certain phrases and words that associate text with a predefined subject
    categories = ["freedom of speech", "healthcare", "taxes", "budget", "net neutrality", "russia", "immigration", "environmnent", "reproductive rights", "guns", "voting rights", "black lives matter", "police brutality", "LGBT"]
    matchers = {"freedom of speech": r"first amendment", "healthcare":r"\baca\b|healthcare|health care|medicaid|health insurance|trumpcare|obamacare", "taxes":r"taxes|tax plan|tax bill", "budget":r"budget plan", "net neutrality":r"fcc|ajit pai", "russia":r"russia investigation", "voting rights":r"voting rights", "immigration":r"\bice\b|\bdaca\b|dreamers", "environmnent":r"climate change|climate justice|endangered species|\bepa\b", "reproductive rights":r"abortion|contraception|planned parenthood", "guns":r"\bnra\b|gun control", "LGBT": r"lgbt|lgbtqa|lgbtq| transgender", "black lives matter": r"black lives matter|#blacklivesmatter", "police brutality": r"police (shooting|brutality)"}
    script_tags = ""
    found_strings = ""
    output_row = []
    for category in categories:
      searchObj = re.findall(matchers[category], text)
      if searchObj:
        script_tags += category + ", "
        found_strings += str(searchObj)
    output_row.append(script_tags)
    output_row.append(found_strings)
    return output_row


if __name__ == '__main__':
    #email = "Do you like your water drinkable and your air breathable? Scott Pruitt is set to dismantle the EPA. Pruitt is a Koch brothers plant who does not believe the EPA should exist. For a rundown of why he is so scary, see our Action 49.• 5 min: Tweet or Facebook these tags: #SaveLivesStopPruitt #PollutingPruitt• 10 minutes: See below for a shortened list of retweets and articles to post on FB. We spelled it all out for you! Just repost.• 20 minutes or more: Here's the full list of things to tweet, superb resource.WHAT YOU CAN DOTweet these tags:POLLUTINGPRUITT #SAVELIVESSTOPPRUITT @REJECTPRUITTRetweet these tweets from your own account:https://twitter.com/SenBrianSchatz/status/821748077161775104https://twitter.com/SenBookerOffice/status/821764129291698184https://twitter.com/SenJeffMerkley/status/821754145006878721https://twitter.com/SenatorCarper/status/821760566360473604https://twitter.com/SenSanders/status/821772916631207949https://twitter.com/SenSanders/status/821775415941341184https://twitter.com/SenJeffMerkley/status/821754145006878721https://twitter.com/maziehirono/status/821802938939174918https://twitter.com/SenGillibrand/status/821803443954339842https://twitter.com/SenBobCasey/status/821818495147118592https://twitter.com/brianschatz/status/821792555574628357https://twitter.com/SenCortezMasto/status/821773402449072128Tweet these graphics to these senators--Download a graphic from this folder--tweet one to each of these Republican senator handles@SenatorCollins, @SenDeanHeller, @SenDonnelly, @SenatorHeitkamp, @SenBobCorker, @SenAlexander, @SenJohnMcCain, @JeffFlakePosts for FacebookPOLLUTINGPRUITT DOESN'T BELIEVE IN MAINSTREAM CLIMATE SCIENCE HTTP://LAT.MS/2K4Y4ET #SAVELIVESRESISTPRUITTPOLLUTINGPRUITT HAS DEEP INDUSTRY TIES. KEEP HIM FROM KILLING US SLOWLY. HTTP://WAPO.ST/2K4V0ZF #SAVELIVESRESISTPRUITTSenator Gillibrand defended our right to a healthy future during #PollutingPruitt’s EPA confirmation hearing. http://wapo.st/2joPXUmTag Susan Collins in these two articles"
    #email = "Now Is Exactly the Time to Talk about Gun Control The White House wants to avoid this conversation in the aftermath of the horrifying and worst mass shooting yet in our country.Simply put: semiautomatic weapons, which can be modified to act as banned automatics using legal products like bump stocks—are weapons of mass destruction. Why are we surprised when someone, including the Vegas shooter, uses one as such?No matter your position on owning guns, we think you can agree with us on this: no one needs guns that can shoot 800 rounds per minute.Asking for gun regulation is not politicizing a tragedy. It is tragedy prevention. It is a logical, caring, and human response. Its hard to see how anyone could see it differently. Thoughts and prayers arent going to do a single thing in this situation, or prevent the next one.There is an immediate way you can let your legislators know what you think of the role government plays in this type of regulation. The House was set to vote this week on a new gun bill that makes silencers available for purchase by anyone, meaning in some states those without background checks. . Noise is what alerts people to a shooting--the noise of gun shots saves lives. Of course, the bad optics of this week means House Republicans have taken that bill off the floor.Let them know you noticed and you refuse to let them make legislative handouts to the gun lobby, and that you expect something to be done about the current lax state of gun regulation in this country. Well write more as more action surfaces in opposition to weapons of mass destruction.1. CALL YOUR REPRESENTATIVE 202-224-3121 and tell them you are paying attention to the vote on silencers, as well as future action on bump stocks, as per the script below.2. FORWARD THIS EMAIL to gun owners you may know. Truth is, most of us dont care about your hunting gun, we just dont want to get shot with an automatic rifle.Use this script (feel free to ad-lib, of course, or modify per your position on gun ownership)I am calling to let you know that I am closely watching the bill about gun silencers, even though it was taken off the House floor this week. I also expect you to introduce legislation that addresses the use of products that can convert semiautomatic weapons into fully automatic ones, just like the Vegas shooter used. I understand these capabilities are considered fun by some, but these weapons of mass destruction have no place among humans, and until we can guarantee that they never fall into the right hands, which is impossible, they should be banned. Responsible gun ownership is possible, I expect you to act accordingly to create guidelines to regulate that.WHY ITS IMPORTANT THIS THIS AND THIS"
    c = EmailCategorizor("DGB.csv")
    emails = c.readEmails()
    with open("DGB_test_output.csv", "w") as csv_file:
      writer = csv.writer(csv_file)
      for email in emails:
        full_row = []
        email_text = c.cleanseText(email["email"])
        action_type_row = c.classifyAction(email_text)
        subject_row = c.classifySubject(email_text)
        full_row.append(email_text)
        full_row = full_row + action_type_row
        full_row = full_row + subject_row
        #print(full_row)
        writer.writerow(full_row)




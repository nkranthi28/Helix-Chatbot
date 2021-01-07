import matplotlib.pyplot as plt
import io
import json
import base64
# import apiai
import os
# import dialogflow
# from flask import Response
# from matplotlib.figure import Figure
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
# from google.api_core.exceptions import InvalidArgument

# Twilio account info
account_sid = "******"
auth_token = "*******"
account_num = "+12133206603"

user_name = ""

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {'https': os.environ['https_proxy']}

client = Client(account_sid, auth_token, http_client=proxy_client)

#database connection
import mysql.connector

mydb = mysql.connector.connect(
  host="knuthala.mysql.pythonanywhere-services.com",
  user="knuthala",
  passwd="*******",
  database="knuthala$default"
)

mycursor = mydb.cursor()

sql_0 = "DROP TABLE IF EXISTS Users"
sql_1 = "DROP TABLE IF EXISTS Headache"
sql_2 = "DROP TABLE IF EXISTS Medication"
sql_3 = "DROP TABLE IF EXISTS Response"

mycursor.execute(sql_0)
mycursor.execute(sql_1)
mycursor.execute(sql_2)
mycursor.execute(sql_3)

#Datbase table creation
mycursor.execute("CREATE TABLE IF NOT EXISTS Users (u_id VARCHAR(25) PRIMARY KEY, First_name VARCHAR(255) NOT NULL, Last_name VARCHAR(255) NOT NULL, Gender VARCHAR(255) NOT NULL, Email VARCHAR(255) NOT NULL UNIQUE, Username VARCHAR(255) NOT NULL UNIQUE, Password VARCHAR(255) NOT NULL, Role VARCHAR(60),Status VARCHAR(60))")
mycursor.execute("CREATE TABLE IF NOT EXISTS Headache (h_id VARCHAR(25) PRIMARY KEY,u_id VARCHAR(25) NOT NULL, Headache_name VARCHAR(255) NOT NULL, Wokeupwith VARCHAR(255) NOT NULL, Duration VARCHAR(255) NOT NULL, Severity VARCHAR(255) NOT NULL, Num_times VARCHAR(255) NOT NULL,Facility VARCHAR(255), M_cycle VARCHAR(255), Ts TIMESTAMP)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Medication (m_id VARCHAR(25) PRIMARY KEY,h_id VARCHAR(25) NOT NULL, Medication_name VARCHAR(255) NOT NULL, Pills VARCHAR(255) NOT NULL, Prior_medication_severity VARCHAR(255) NOT NULL)")
mycursor.execute("CREATE TABLE IF NOT EXISTS Response (r_id VARCHAR(25) PRIMARY KEY,u_id VARCHAR(25) NOT NULL,h_id VARCHAR(25),m_id VARCHAR(25), QuestionText VARCHAR(255) NOT NULL, Response_Text VARCHAR(255) NOT NULL)")

sql_0 = "INSERT INTO Users (u_id, First_name, Last_name, Gender, Email, Username, Password, Role, Status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
val_0 = [
  ('1', "John","Wick","Male","jwick@usc.edu","john_wick","jp#2Gus^+=5wf2N_", "User","Active"),
  ('2', "Jonna","Wane","Female","jwane@usc.edu","jonna_1234","nR5z@8s","User","Active"),
  ('3', "Kane","Wane","Male","kwane@usc.edu","kwane","d!DF7pc7p+fKz^&w","User","Suspended"),
  ('4', "Jon","William","Male","jwilliam@usc.edu","jonwill","goodwill@1298","User","Active"),
  ('5', "Jane","Len","Female","jlen@usc.edu","jane123","gdGMm2H=2&NsVTU!","User","Suspended"),
  ('6', "Katherine","Jo","Female","kjo@usc.edu","admin","admin","Admin","Active"),
  ('7', "Kathy","Jo","Female","kj@usc.edu","admin1","admin1","Admin","Active")
]

mycursor.executemany(sql_0, val_0)
mydb.commit()

sql = "INSERT INTO Headache (h_id,u_id,Headache_name,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle,Ts) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s,%s)"
val = [
  ('1', '1','Sinus Headache','Yes','5 hours','Moderate','1','Yes,USC','','2019-08-01 02:03:40'),
  ('2', '1','Chatbot','Yes','21 hours','Mild','1','Yes','','2019-06-03 03:10:30'),
  ('3', '1','Migraine','No','10 hours','Severe','2','USC','','2019-11-01 12:22:00'),
  ('4', '2','Stress','No','10 hours','Mild','1','USC','Middle','2020-03-20 02:55:00'),
  ('5', '2','Tension','No','12 hours','Moderate','1','USC','Middle','2020-07-21 02:18:00'),
  ('6', '2','Migraine','Yes','15 hours','Mild','1','USC','Middle','2020-09-01 18:40:00'),
  ('7', '3','Work-related','No','2 hours','Moderate','1','USC','','2020-05-05 09:10:09'),
  ('8', '3','Project','No','5 hours','Mild','2','USC','','2020-05-07 11:50:42'),
  ('9', '3','Stress','No','7 hours','Moderate','3','USC','','2020-05-08 18:27:32'),
  ('10', '4','Exams','Yes','1 hours','Moderate','1','','','2020-02-02 12:10:00'),
  ('11', '4','AI','Yes','2 hours','Moderate','2','','','2020-02-20 23:50:20'),
  ('12', '4','Migraine','No','5 hours','Mild','1','','','2020-03-24 20:20:24'),
  ('13', '5','Fever Headache','No','8 hours','Mild','1','St.Thomas Hospital','Close','2020-01-01 07:30:00'),
  ('14', '5','Flu','No','10 hours','Moderate','2','St.Thomas Hospital','Close','2020-02-01 10:20:00'),
  ('15', '5','Sinus Headache','Yes','24 hours','Severe','1','St.Thomas Hospital','Close','2020-03-01 14:10:10')
]

mycursor.executemany(sql, val)
mydb.commit()

sql1 = "INSERT INTO Medication (m_id,h_id,Medication_name,Pills,Prior_medication_severity) VALUES (%s, %s, %s, %s, %s)"
val1 = [
  ('1', '1','aspirin','1','VerySevere'),
  ('2', '1','aspirin','1','Moderate'),
  ('3', '1','ibuprofen','2','Moderate'),
  ('4', '1','ibuprofen','1','Moderate'),
  ('5', '2','ibuprofen','1','Verysevere'),
  ('6', '2','ibuprofen','1','Severe'),
  ('7', '2','Aleve','1','Moderate'),
  ('8', '2','Aleve','2','Mild'),
  ('9', '3','aspirin','1','Moderate'),
  ('10', '3','aspirin','1','Mild'),
  ('11', '3','ibuprofen','2','Mild'),
  ('12', '3','ibuprofen','1','Mild'),
  ('13', '4','naproxen','1','Moderate'),
  ('14', '4','naproxen','2','Moderate'),
  ('15', '4','naproxen','1','Mild'),
  ('16', '4','naproxen','1','Mild'),
  ('17', '5','Aleve','1','Moderate'),
  ('18', '5','Aleve','1','Moderate'),
  ('19', '5','Aleve','1','Moderate'),
  ('20', '5','Aleve','1','Moderate'),
  ('21', '6','naproxen','1','Severe'),
  ('22', '6','naproxen','1','Severe'),
  ('23', '6','naproxen','1','Mild'),
  ('24', '6','naproxen','1','Mild'),
  ('25', '7','Advil','1','Severe'),
  ('26', '7','Advil','1','Severe'),
  ('27', '7','Advil','1','Moderate'),
  ('28', '7','Advil','1','Moderate'),
  ('29', '8','Motrin','1','Severe'),
  ('30', '8','Motrin','1','Severe'),
  ('31', '8','Motrin','1','Moderate'),
  ('32', '8','Motrin','1','Mild'),
  ('33', '9','indomethacin','1','Severe'),
  ('34', '9','indomethacin','1','Moderate'),
  ('35', '9','indomethacin','1','Moderate'),
  ('36', '9','indomethacin','1','Moderate'),
  ('37', '10','ketorolac','1','Severe'),
  ('38', '10','ketorolac','1','Severe'),
  ('39', '10','ketorolac','1','Severe'),
  ('40', '10','ketorolac','1','Moderate'),
  ('41', '11','Motrin','1','Severe'),
  ('42', '11','Motrin','1','Severe'),
  ('43', '11','Motrin','1','Moderate'),
  ('44', '11','Aleve','1','Moderate'),
  ('45', '12','naproxen','1','Severe'),
  ('46', '12','naproxen','1','Severe'),
  ('47', '12','Aleve','1','Mild'),
  ('48', '12','naproxen','1','Mild'),
  ('49', '13','Advil','1','Severe'),
  ('50', '13','Advil','1','Severe'),
  ('51', '13','Motrin','1','Mild'),
  ('52', '13','Motrin','1','Mild'),
  ('53', '14','indomethacin','1','Verysevere'),
  ('54', '14','indomethacin','1','Verysevere'),
  ('55', '14','Aleve','1','Moderate'),
  ('56', '14','naproxen','1','Moderate'),
  ('57', '15','indomethacin','1','Verysevere'),
  ('58', '15','Advil','1','Severe'),
  ('59', '15','naproxen','1','Moderate'),
  ('60', '15','Aleve','1','Mild')
]


mycursor.executemany(sql1, val1)
mydb.commit()

s2 = "INSERT INTO Response (r_id,u_id,h_id,m_id,QuestionText,Response_Text) VALUES (%s, %s, %s, %s, %s, %s)"
v2 = [
  ('1', '1','1','','what name do you give this headache?','Sinus Headache'),
  ('2', '1','1','','Did you wake up with this headache?','Yes'),
  ('3', '1','1','','What is/was the duration of your headache?','5 hours'),
  ('4', '1','1','','How severe is your headache?','Moderate'),
  ('5', '1','1','','How many times has it happened since you wokeup?','1'),
  ('6', '1','1','','Was it a USC facility','Yes,USC'),
  ('7', '1','1','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('8', '1','1','1','What medication was it?','aspirin'),
  ('9', '1','1','1','How many pills?','1'),
  ('10', '1','1','1','How severe was your headache prior to medication?','VerySevere'),
  ('11', '1','1','2','What medication was it?','aspirin'),
  ('12', '1','1','2','How many pills?','1'),
  ('13', '1','1','2','How severe was your headache prior to medication?','Moderate'),
  ('14', '1','1','3','What medication was it?','ibuprofen'),
  ('15', '1','1','3','How many pills?','2'),
  ('16', '1','1','3','How severe was your headache prior to medication?','Moderate'),
  ('17', '1','1','4','What medication was it?','ibuprofen'),
  ('18', '1','1','4','How many pills?','1'),
  ('19', '1','1','4','How severe was your headache prior to medication?','Moderate'),
  ('20', '1','2','','what name do you give this headache?','Chatbot'),
  ('21', '1','2','','Did you wake up with this headache?','Yes'),
  ('22', '1','2','','What is/was the duration of your headache?','21 hours'),
  ('23', '1','2','','How severe is your headache?','Mild'),
  ('24', '1','2','','How many times has it happened since you wokeup?','1'),
  ('25', '1','2','','Was it a USC facility','Yes'),
  ('26', '1','2','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('27', '1','2','5','What medication was it?','ibuprofen'),
  ('28', '1','2','5','How many pills?','1'),
  ('29', '1','2','5','How severe was your headache prior to medication?','VerySevere'),
  ('30', '1','2','6','What medication was it?','ibuprofen'),
  ('31', '1','2','6','How many pills?','1'),
  ('32', '1','2','6','How severe was your headache prior to medication?','Severe'),
  ('33', '1','2','7','What medication was it?','Aleve'),
  ('34', '1','2','7','How many pills?','1'),
  ('35', '1','2','7','How severe was your headache prior to medication?','Moderate'),
  ('36', '1','2','8','What medication was it?','Aleve'),
  ('37', '1','2','8','How many pills?','2'),
  ('38', '1','2','8','How severe was your headache prior to medication?','Mild'),
  ('39', '1','3','','what name do you give this headache?','Migraine'),
  ('40', '1','3','','Did you wake up with this headache?','No'),
  ('41', '1','3','','What is/was the duration of your headache?','10 hours'),
  ('42', '1','3','','How severe is your headache?','Mild'),
  ('43', '1','3','','How many times has it happened since you wokeup?','2'),
  ('44', '1','3','','Was it a USC facility','USC'),
  ('45', '1','3','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('46', '1','3','9','What medication was it?','aspirin'),
  ('47', '1','3','9','How many pills?','1'),
  ('48', '1','3','9','How severe was your headache prior to medication?','Moderate'),
  ('49', '1','3','10','What medication was it?','aspirin'),
  ('50', '1','3','10','How many pills?','1'),
  ('51', '1','3','10','How severe was your headache prior to medication?','Mild'),
  ('52', '1','3','11','What medication was it?','ibuprofen'),
  ('53', '1','3','11','How many pills?','2'),
  ('54', '1','3','11','How severe was your headache prior to medication?','Mild'),
  ('55', '1','3','12','What medication was it?','ibuprofen'),
  ('56', '1','3','12','How many pills?','1'),
  ('57', '1','3','12','How severe was your headache prior to medication?','Mild'),
  ('58', '2','4','','what name do you give this headache?','Stress'),
  ('59', '2','4','','Did you wake up with this headache?','No'),
  ('60', '2','4','','What is/was the duration of your headache?','10 hours'),
  ('61', '2','4','','How severe is your headache?','Moderate'),
  ('62', '2','4','','How many times has it happened since you wokeup?','1'),
  ('63', '2','4','','Was it a USC facility','USC'),
  ('64', '2','4','','If female, are you in the middle or close to your menstruation cycle?','Middle'),
  ('65', '2','4','13','What medication was it?','naproxen'),
  ('66', '2','4','13','How many pills?','1'),
  ('67', '2','4','13','How severe was your headache prior to medication?','Moderate'),
  ('68', '2','4','14','What medication was it?','naproxen'),
  ('69', '2','4','14','How many pills?','2'),
  ('70', '2','4','14','How severe was your headache prior to medication?','Moderate'),
  ('71', '2','4','15','What medication was it?','naproxen'),
  ('72', '2','4','15','How many pills?','1'),
  ('73', '2','4','15','How severe was your headache prior to medication?','Mild'),
  ('74', '2','4','16','What medication was it?','naproxen'),
  ('75', '2','4','16','How many pills?','1'),
  ('76', '2','4','16','How severe was your headache prior to medication?','Mild'),
  ('77', '2','5','','what name do you give this headache?','Tension'),
  ('78', '2','5','','Did you wake up with this headache?','No'),
  ('79', '2','5','','What is/was the duration of your headache?','12 hours'),
  ('80', '2','5','','How severe is your headache?','Moderate'),
  ('81', '2','5','','How many times has it happened since you wokeup?','1'),
  ('82', '2','5','','Was it a USC facility','USC'),
  ('83', '2','5','','If female, are you in the middle or close to your menstruation cycle?','Middle'),
  ('84', '2','5','17','What medication was it?','Aleve'),
  ('85', '2','5','17','How many pills?','1'),
  ('86', '2','5','17','How severe was your headache prior to medication?','Moderate'),
  ('87', '2','5','18','What medication was it?','Aleve'),
  ('88', '2','5','18','How many pills?','1'),
  ('89', '2','5','18','How severe was your headache prior to medication?','Moderate'),
  ('90', '2','5','19','What medication was it?','Aleve'),
  ('91', '2','5','19','How many pills?','1'),
  ('92', '2','5','19','How severe was your headache prior to medication?','Moderate'),
  ('93', '2','5','20','What medication was it?','Aleve'),
  ('94', '2','5','20','How many pills?','1'),
  ('95', '2','5','20','How severe was your headache prior to medication?','Moderate'),
  ('96', '2','6','','what name do you give this headache?','Migraine'),
  ('97', '2','6','','Did you wake up with this headache?','Yes'),
  ('98', '2','6','','What is/was the duration of your headache?','15 hours'),
  ('99', '2','6','','How severe is your headache?','Mild'),
  ('100', '2','6','','How many times has it happened since you wokeup?','1'),
  ('101', '2','6','','Was it a USC facility','USC'),
  ('102', '2','6','','If female, are you in the middle or close to your menstruation cycle?','Middle'),
  ('103', '2','6','21','What medication was it?','naproxen'),
  ('104', '2','6','21','How many pills?','1'),
  ('105', '2','6','21','How severe was your headache prior to medication?','Severe'),
  ('106', '2','6','22','What medication was it?','naproxen'),
  ('107', '2','6','22','How many pills?','1'),
  ('108', '2','6','22','How severe was your headache prior to medication?','Severe'),
  ('109', '2','6','23','What medication was it?','naproxen'),
  ('110', '2','6','23','How many pills?','1'),
  ('111', '2','6','23','How severe was your headache prior to medication?','Mild'),
  ('112', '2','6','24','What medication was it?','naproxen'),
  ('113', '2','6','24','How many pills?','1'),
  ('114', '2','6','24','How severe was your headache prior to medication?','Mild'),
  ('115', '3','7','','what name do you give this headache?','Work-related'),
  ('116', '3','7','','Did you wake up with this headache?','No'),
  ('117', '3','7','','What is/was the duration of your headache?','2 hours'),
  ('118', '3','7','','How severe is your headache?','Moderate'),
  ('119', '3','7','','How many times has it happened since you wokeup?','1'),
  ('120', '3','7','','Was it a USC facility','USC'),
  ('121', '3','7','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('122', '3','7','25','What medication was it?','Advil'),
  ('123', '3','7','25','How many pills?','1'),
  ('124', '3','7','25','How severe was your headache prior to medication?','Severe'),
  ('125', '3','7','26','What medication was it?','Advil'),
  ('126', '3','7','26','How many pills?','1'),
  ('127', '3','7','26','How severe was your headache prior to medication?','Severe'),
  ('128', '3','7','27','What medication was it?','Advil'),
  ('129', '3','7','27','How many pills?','1'),
  ('130', '3','7','27','How severe was your headache prior to medication?','Moderate'),
  ('131', '3','7','28','What medication was it?','Advil'),
  ('132', '3','7','28','How many pills?','1'),
  ('133', '3','7','28','How severe was your headache prior to medication?','Moderate'),
  ('134', '3','8','','what name do you give this headache?','Project'),
  ('135', '3','8','','Did you wake up with this headache?','No'),
  ('136', '3','8','','What is/was the duration of your headache?','5 hours'),
  ('137', '3','8','','How severe is your headache?','Mild'),
  ('138', '3','8','','How many times has it happened since you wokeup?','2'),
  ('139', '3','8','','Was it a USC facility','USC'),
  ('140', '3','8','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('141', '3','8','29','What medication was it?','Motrin'),
  ('142', '3','8','29','How many pills?','1'),
  ('143', '3','8','29','How severe was your headache prior to medication?','Severe'),
  ('144', '3','8','30','What medication was it?','Motrin'),
  ('145', '3','8','30','How many pills?','1'),
  ('146', '3','8','30','How severe was your headache prior to medication?','Severe'),
  ('147', '3','8','31','What medication was it?','Motrin'),
  ('148', '3','8','31','How many pills?','1'),
  ('149', '3','8','31','How severe was your headache prior to medication?','Moderate'),
  ('150', '3','8','32','What medication was it?','Motrin'),
  ('151', '3','8','32','How many pills?','1'),
  ('152', '3','8','32','How severe was your headache prior to medication?','Mild'),
  ('153', '3','9','','what name do you give this headache?','Stress'),
  ('154', '3','9','','Did you wake up with this headache?','No'),
  ('155', '3','9','','What is/was the duration of your headache?','7 hours'),
  ('156', '3','9','','How severe is your headache?','Moderte'),
  ('157', '3','9','','How many times has it happened since you wokeup?','3'),
  ('158', '3','9','','Was it a USC facility','USC'),
  ('159', '3','9','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('160', '3','9','33','What medication was it?','indomethacin'),
  ('161', '3','9','33','How many pills?','1'),
  ('162', '3','9','33','How severe was your headache prior to medication?','Severe'),
  ('163', '3','9','34','What medication was it?','indomethacin'),
  ('164', '3','9','34','How many pills?','1'),
  ('165', '3','9','34','How severe was your headache prior to medication?','Moderate'),
  ('166', '3','9','35','What medication was it?','indomethacin'),
  ('167', '3','9','35','How many pills?','1'),
  ('168', '3','9','35','How severe was your headache prior to medication?','Moderate'),
  ('169', '3','9','36','What medication was it?','indomethacin'),
  ('170', '3','9','36','How many pills?','1'),
  ('171', '3','9','36','How severe was your headache prior to medication?','Moderate'),
  ('172', '4','10','','what name do you give this headache?','Exams'),
  ('173', '4','10','','Did you wake up with this headache?','Yes'),
  ('174', '4','10','','What is/was the duration of your headache?','1 hours'),
  ('175', '4','10','','How severe is your headache?','Moderte'),
  ('176', '4','10','','How many times has it happened since you wokeup?','1'),
  ('177', '4','10','','Was it a USC facility',''),
  ('178', '4','10','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('179', '4','10','37','What medication was it?','ketorolac'),
  ('180', '4','10','37','How many pills?','1'),
  ('181', '4','10','37','How severe was your headache prior to medication?','Severe'),
  ('182', '4','10','38','What medication was it?','ketorolac'),
  ('183', '4','10','38','How many pills?','1'),
  ('184', '4','10','38','How severe was your headache prior to medication?','Severe'),
  ('185', '4','10','39','What medication was it?','ketorolac'),
  ('186', '4','10','39','How many pills?','1'),
  ('187', '4','10','39','How severe was your headache prior to medication?','Severe'),
  ('188', '4','10','40','What medication was it?','ketorolac'),
  ('189', '4','10','40','How many pills?','1'),
  ('190', '4','10','40','How severe was your headache prior to medication?','Moderate'),
  ('191', '4','11','','what name do you give this headache?','AI'),
  ('192', '4','11','','Did you wake up with this headache?','Yes'),
  ('193', '4','11','','What is/was the duration of your headache?','2 hours'),
  ('194', '4','11','','How severe is your headache?','Moderte'),
  ('195', '4','11','','How many times has it happened since you wokeup?','2'),
  ('196', '4','11','','Was it a USC facility',''),
  ('197', '4','11','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('198', '4','11','41','What medication was it?','Motrin'),
  ('199', '4','11','41','How many pills?','1'),
  ('200', '4','11','41','How severe was your headache prior to medication?','Severe'),
  ('201', '4','11','42','What medication was it?','Motrin'),
  ('202', '4','11','42','How many pills?','1'),
  ('203', '4','11','42','How severe was your headache prior to medication?','Severe'),
  ('204', '4','11','43','What medication was it?','Motrin'),
  ('205', '4','11','43','How many pills?','1'),
  ('206', '4','11','43','How severe was your headache prior to medication?','Moderate'),
  ('207', '4','11','44','What medication was it?','Aleve'),
  ('208', '4','11','44','How many pills?','1'),
  ('209', '4','11','44','How severe was your headache prior to medication?','Moderate'),
  ('210', '4','12','','what name do you give this headache?','Migraine'),
  ('211', '4','12','','Did you wake up with this headache?','No'),
  ('212', '4','12','','What is/was the duration of your headache?','5 hours'),
  ('213', '4','12','','How severe is your headache?','Mild'),
  ('214', '4','12','','How many times has it happened since you wokeup?','1'),
  ('215', '4','12','','Was it a USC facility',''),
  ('216', '4','12','','If female, are you in the middle or close to your menstruation cycle?',''),
  ('217', '4','12','45','What medication was it?','naproxen'),
  ('218', '4','12','45','How many pills?','1'),
  ('219', '4','12','45','How severe was your headache prior to medication?','Severe'),
  ('220', '4','12','46','What medication was it?','naproxen'),
  ('221', '4','12','46','How many pills?','1'),
  ('222', '4','12','46','How severe was your headache prior to medication?','Severe'),
  ('223', '4','12','47','What medication was it?','Aleve'),
  ('224', '4','12','47','How many pills?','1'),
  ('225', '4','12','47','How severe was your headache prior to medication?','Mild'),
  ('226', '4','12','48','What medication was it?','naproxen'),
  ('227', '4','12','48','How many pills?','1'),
  ('228', '4','12','48','How severe was your headache prior to medication?','Mild'),
  ('229', '5','13','','what name do you give this headache?','Fever Headache'),
  ('230', '5','13','','Did you wake up with this headache?','No'),
  ('231', '5','13','','What is/was the duration of your headache?','8 hours'),
  ('232', '5','13','','How severe is your headache?','Mild'),
  ('233', '5','13','','How many times has it happened since you wokeup?','1'),
  ('234', '5','13','','Was it a USC facility','St.Thomas Hospital'),
  ('235', '5','13','','If female, are you in the middle or close to your menstruation cycle?','Close'),
  ('236', '5','13','49','What medication was it?','Advil'),
  ('237', '5','13','49','How many pills?','1'),
  ('238', '5','13','49','How severe was your headache prior to medication?','Severe'),
  ('239', '5','13','50','What medication was it?','Advil'),
  ('240', '5','13','50','How many pills?','1'),
  ('241', '5','13','50','How severe was your headache prior to medication?','Severe'),
  ('242', '5','13','51','What medication was it?','Motrin'),
  ('243', '5','13','51','How many pills?','1'),
  ('244', '5','13','51','How severe was your headache prior to medication?','Mild'),
  ('245', '5','13','52','What medication was it?','Motrin'),
  ('246', '5','13','52','How many pills?','1'),
  ('247', '5','13','52','How severe was your headache prior to medication?','Mild'),
  ('248', '5','14','','what name do you give this headache?','Flu'),
  ('249', '5','14','','Did you wake up with this headache?','No'),
  ('250', '5','14','','What is/was the duration of your headache?','10 hours'),
  ('251', '5','14','','How severe is your headache?','Moderate'),
  ('252', '5','14','','How many times has it happened since you wokeup?','2'),
  ('253', '5','14','','Was it a USC facility','St.Thomas Hospital'),
  ('254', '5','14','','If female, are you in the middle or close to your menstruation cycle?','Close'),
  ('255', '5','14','53','What medication was it?','indomethacin'),
  ('256', '5','14','53','How many pills?','1'),
  ('257', '5','14','53','How severe was your headache prior to medication?','Severe'),
  ('258', '5','14','54','What medication was it?','indomethacin'),
  ('259', '5','14','54','How many pills?','1'),
  ('260', '5','14','54','How severe was your headache prior to medication?','Severe'),
  ('261', '5','14','55','What medication was it?','Aleve'),
  ('262', '5','14','55','How many pills?','1'),
  ('263', '5','14','55','How severe was your headache prior to medication?','Moderate'),
  ('264', '5','14','56','What medication was it?','naproxen'),
  ('265', '5','14','56','How many pills?','1'),
  ('266', '5','14','56','How severe was your headache prior to medication?','Moderate'),
  ('267', '5','15','','what name do you give this headache?','Sinus Headache'),
  ('268', '5','15','','Did you wake up with this headache?','Yes'),
  ('269', '5','15','','What is/was the duration of your headache?','24 hours'),
  ('270', '5','15','','How severe is your headache?','Severe'),
  ('271', '5','15','','How many times has it happened since you wokeup?','1'),
  ('272', '5','15','','Was it a USC facility','St.Thomas Hospital'),
  ('273', '5','15','','If female, are you in the middle or close to your menstruation cycle?','Close'),
  ('274', '5','15','57','What medication was it?','indomethacin'),
  ('275', '5','15','57','How many pills?','1'),
  ('276', '5','15','57','How severe was your headache prior to medication?','Verysevere'),
  ('277', '5','15','58','What medication was it?','Advil'),
  ('278', '5','15','58','How many pills?','1'),
  ('279', '5','15','58','How severe was your headache prior to medication?','Severe'),
  ('280', '5','15','59','What medication was it?','naproxen'),
  ('281', '5','15','59','How many pills?','1'),
  ('282', '5','15','59','How severe was your headache prior to medication?','Moderate'),
  ('283', '5','15','60','What medication was it?','Aleve'),
  ('284', '5','15','60','How many pills?','1'),
  ('285', '5','15','60','How severe was your headache prior to medication?','Mild')
]

mycursor.executemany(s2, v2)
mydb.commit()

# # api.ai account info
# CLIENT_ACCESS_TOKEN = "d3ada2ac84f84769b11f99c9c4500b37"
# ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

# initialize the flask app
app = Flask(__name__)
# app.config['SESSION_COOKIE_SECURE'] = False

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('start.html',title='CSCI 485 Intelligent Chatbot Login Page Tutorial')

@app.route('/start', methods=['GET', 'POST'])
def start():
    if request.method == 'POST':
        val=request.form['role']
        if val=='Admin':
            return render_template('login.html')
        elif val=='User':
            return render_template('patient.html')

@app.route('/patient', methods=['GET', 'POST'])
def patient():
    #fetching Username and password from database for admin
    mycursor.execute ("select Username,Password from Users where Username!='admin'")
    data = mycursor.fetchall ()
    #Storing the username and password fetched into dictionary
    # dict={}
    user_pwd={}
    for row in data:
        user_pwd[row[0]]= row[1]
    #Obtaining the values that the user input
    userName = request.values.get("uname", None)
    userPasswd = request.values.get("passwd", None)
    #checking if the password matches the admin password
    if userName in user_pwd and userPasswd == user_pwd[userName]:
        if userName=='john_wick':
            return render_template('John_data.html',title='CSCI 485 Intelligent Chatbot Login Page Tutorial')
        elif userName=='jonna_1234':
            return render_template('Jonna_data.html',title='CSCI 485 Intelligent Chatbot Login Page Tutorial')
        elif userName=='kwane':
            return render_template('Kane_data.html',title='CSCI 485 Intelligent Chatbot Login Page Tutorial')
        elif userName=='jonwill':
            return render_template('Jon_data.html',title='CSCI 485 Intelligent Chatbot Login Page Tutorial')
        elif userName=='jane123':
            return render_template('Jane_data.html',title='CSCI 485 Intelligent Chatbot Login Page Tutorial')
    else:
        return render_template('patient.html')

@app.route('/visualize', methods=['GET', 'POST'])
def visualize():
    if request.method == 'POST':
        selectedValue=request.form['parameter']
        if selectedValue=='Severity':
            #extracting severity as a numerical value
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='1'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='1'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            #Bar graph plotting
            plt.clf()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            # plt.legend(loc="upper left")
            # plt.legend(handles=(labels, new_data),labels=('label1', 'label2'),loc='upper left')
            img = io.BytesIO()
            plt.bar(labels, new_data, width=0.8)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #Line graph plotting
            #Clears the current figure
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            plt.plot(labels, new_data)
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            #returning two images
            return render_template('test.html',plot_url=plot_url, plot_url1=plot_url1)
        elif selectedValue=='Time':
            mycursor.execute ("select Ts from Headache where u_id='1'")
            time = mycursor.fetchall ()
            time=[i[0] for i in time]
            mycursor.execute ("select Headache_name from Headache where u_id='1'")
            name = mycursor.fetchall ()
            name=[i[0] for i in name]
            #scatter plot
            plt.clf()
            img = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            plt.scatter(time,name,color=['red','green','blue'])
            #Adjusts the subplot(s) to fit in the figure area
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #line chart
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            # plt.barh(time,name, align='center', alpha=0.5, height=0.8)
            plt.plot(time, name, c='xkcd:baby poop green')
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            return render_template('Num_Headache.html',plot_url=plot_url,plot_url1=plot_url1)
        elif selectedValue=='Wokeup':
            #pie_chart
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='Yes' and u_id='1'")
            val = mycursor.fetchall ()
            val=[i[0] for i in val]
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='No' and u_id='1'")
            count = mycursor.fetchall ()
            count=[i[0] for i in count]
            piechart=[]
            piechart.append(val[0])
            piechart.append(count[0])
            activities = ['Yes','No']
            cols = ['c','m']
            plt.clf()
            plt.pie(piechart,labels=activities,colors=cols,startangle=90,shadow= True,autopct='%1.1f%%')
            plt.title('Woke up with Headache', fontsize=20)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('wokeup.html',plot_url=plot_url)
        elif selectedValue=='Duration':
            #Bubble_chart
            mycursor.execute ("select Duration from Headache where u_id='1'")
            dur = mycursor.fetchall ()
            dur=[i[0] for i in dur]
            #extracting the integer
            int_dur = [int(x[:-6])*60 for x in dur]
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='1'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='1'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            plt.clf()
            plt.scatter(labels, new_data, s=int_dur*1000, alpha=0.5,color=['red','green','blue'])
            # plt.tight_layout()
            img = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Name vs Severity vs Duration', fontsize=20)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('Duration.html',plot_url=plot_url)

@app.route('/visualize_Jonna', methods=['GET', 'POST'])
def visualize_Jonna():
    if request.method == 'POST':
        selectedValue=request.form['parameter']
        if selectedValue=='Severity':
            #extracting severity as a numerical value
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='2'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='2'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            #Bar graph plotting
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            img = io.BytesIO()
            plt.bar(labels, new_data, width=0.8)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #Line graph plotting
            #Clears the current figure
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            plt.plot(labels, new_data)
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            #returning two images
            return render_template('test.html',plot_url=plot_url, plot_url1=plot_url1)
        elif selectedValue=='Time':
            mycursor.execute ("select Ts from Headache where u_id='2'")
            time = mycursor.fetchall ()
            time=[i[0] for i in time]
            mycursor.execute ("select Headache_name from Headache where u_id='2'")
            name = mycursor.fetchall ()
            name=[i[0] for i in name]
            #scatter plot
            img = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            plt.scatter(time,name,color=['red','green','blue'])
            #Adjusts the subplot(s) to fit in the figure area
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            #line chart
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            # plt.barh(time,name, align='center', alpha=0.5, height=0.8)
            plt.plot(time, name, c='xkcd:baby poop green')
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            return render_template('Num_Headache.html',plot_url=plot_url,plot_url1=plot_url1)
        elif selectedValue=='Wokeup':
            #pie_chart
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='Yes' and u_id='2'")
            val = mycursor.fetchall ()
            val=[i[0] for i in val]
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='No' and u_id='2'")
            count = mycursor.fetchall ()
            count=[i[0] for i in count]
            piechart=[]
            piechart.append(val[0])
            piechart.append(count[0])
            activities = ['Yes','No']
            cols = ['c','m']
            plt.clf()
            plt.pie(piechart,labels=activities,colors=cols,startangle=90,shadow= True,autopct='%1.1f%%')
            plt.title('Woke up with Headache', fontsize=20)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('wokeup.html',plot_url=plot_url)
        elif selectedValue=='Duration':
            #Bubble_chart
            mycursor.execute ("select Duration from Headache where u_id='2'")
            dur = mycursor.fetchall ()
            dur=[i[0] for i in dur]
            #extracting the integer
            int_dur = [int(x[:-6])*60 for x in dur]
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='2'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='2'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            plt.clf()
            plt.scatter(labels, new_data, s=int_dur*1000, alpha=0.5,color=['red','green','blue'])
            # plt.tight_layout()
            img = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Name vs Severity vs Duration', fontsize=20)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('Duration.html',plot_url=plot_url)

@app.route('/visualize_Kane', methods=['GET', 'POST'])
def visualize_Kane():
    if request.method == 'POST':
        selectedValue=request.form['parameter']
        if selectedValue=='Severity':
            #extracting severity as a numerical value
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='3'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='3'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            #Bar graph plotting
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            img = io.BytesIO()
            plt.bar(labels, new_data, width=0.8)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #Line graph plotting
            #Clears the current figure
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            plt.plot(labels, new_data)
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            #returning two images
            return render_template('test.html',plot_url=plot_url, plot_url1=plot_url1)
        elif selectedValue=='Time':
            mycursor.execute ("select Ts from Headache where u_id='3'")
            time = mycursor.fetchall ()
            time=[i[0] for i in time]
            mycursor.execute ("select Headache_name from Headache where u_id='3'")
            name = mycursor.fetchall ()
            name=[i[0] for i in name]
            #scatter plot
            img = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            plt.scatter(time,name,color=['red','green','blue'])
            #Adjusts the subplot(s) to fit in the figure area
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            #line chart
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            # plt.barh(time,name, align='center', alpha=0.5, height=0.8)
            plt.plot(time, name, c='xkcd:baby poop green')
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            return render_template('Num_Headache.html',plot_url=plot_url,plot_url1=plot_url1)
        elif selectedValue=='Wokeup':
            #pie_chart
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='Yes' and u_id='3'")
            val = mycursor.fetchall ()
            val=[i[0] for i in val]
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='No' and u_id='3'")
            count = mycursor.fetchall ()
            count=[i[0] for i in count]
            piechart=[]
            piechart.append(val[0])
            piechart.append(count[0])
            activities = ['Yes','No']
            cols = ['c','m']
            plt.clf()
            plt.pie(piechart,labels=activities,colors=cols,startangle=90,shadow= True,autopct='%1.1f%%')
            plt.title('Woke up with Headache', fontsize=20)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('wokeup.html',plot_url=plot_url)
        elif selectedValue=='Duration':
            #Bubble_chart
            mycursor.execute ("select Duration from Headache where u_id='3'")
            dur = mycursor.fetchall ()
            dur=[i[0] for i in dur]
            #extracting the integer
            int_dur = [int(x[:-6])*60 for x in dur]
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='3'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='3'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            plt.clf()
            plt.scatter(labels, new_data, s=int_dur*1000, alpha=0.5,color=['red','green','blue'])
            # plt.tight_layout()
            img = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Name vs Severity vs Duration', fontsize=20)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('Duration.html',plot_url=plot_url)

@app.route('/visualize_Jon', methods=['GET', 'POST'])
def visualize_Jon():
    if request.method == 'POST':
        selectedValue=request.form['parameter']
        if selectedValue=='Severity':
            #extracting severity as a numerical value
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='4'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='4'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            #Bar graph plotting
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            img = io.BytesIO()
            plt.bar(labels, new_data, width=0.8)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #Line graph plotting
            #Clears the current figure
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            plt.plot(labels, new_data)
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            #returning two images
            return render_template('test.html',plot_url=plot_url, plot_url1=plot_url1)
        elif selectedValue=='Time':
            mycursor.execute ("select Ts from Headache where u_id='4'")
            time = mycursor.fetchall ()
            time=[i[0] for i in time]
            mycursor.execute ("select Headache_name from Headache where u_id='4'")
            name = mycursor.fetchall ()
            name=[i[0] for i in name]
            #scatter plot
            img = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            plt.scatter(time,name,color=['red','green','blue'])
            #Adjusts the subplot(s) to fit in the figure area
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            #line chart
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            # plt.barh(time,name, align='center', alpha=0.5, height=0.8)
            plt.plot(time, name, c='xkcd:baby poop green')
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            return render_template('Num_Headache.html',plot_url=plot_url,plot_url1=plot_url1)
        elif selectedValue=='Wokeup':
            #pie_chart
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='Yes' and u_id='4'")
            val = mycursor.fetchall ()
            val=[i[0] for i in val]
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='No' and u_id='4'")
            count = mycursor.fetchall ()
            count=[i[0] for i in count]
            piechart=[]
            piechart.append(val[0])
            piechart.append(count[0])
            activities = ['Yes','No']
            cols = ['c','m']
            plt.clf()
            plt.pie(piechart,labels=activities,colors=cols,startangle=90,shadow= True,autopct='%1.1f%%')
            plt.title('Woke up with Headache', fontsize=20)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('wokeup.html',plot_url=plot_url)
        elif selectedValue=='Duration':
            #Bubble_chart
            mycursor.execute ("select Duration from Headache where u_id='4'")
            dur = mycursor.fetchall ()
            dur=[i[0] for i in dur]
            #extracting the integer
            int_dur = [int(x[:-6])*60 for x in dur]
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='4'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='4'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            plt.clf()
            plt.scatter(labels, new_data, s=int_dur*1000, alpha=0.5,color=['red','green','blue'])
            # plt.tight_layout()
            img = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Name vs Severity vs Duration', fontsize=20)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('Duration.html',plot_url=plot_url)

@app.route('/visualize_Jane', methods=['GET', 'POST'])
def visualize_Jane():
    if request.method == 'POST':
        selectedValue=request.form['parameter']
        if selectedValue=='Severity':
            #extracting severity as a numerical value
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='5'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='5'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            #Bar graph plotting
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            img = io.BytesIO()
            plt.bar(labels, new_data, width=0.8)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            #Line graph plotting
            #Clears the current figure
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Severity vs Headache', fontsize=20)
            plt.plot(labels, new_data)
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            #returning two images
            return render_template('test.html',plot_url=plot_url, plot_url1=plot_url1)
        elif selectedValue=='Time':
            mycursor.execute ("select Ts from Headache where u_id='5'")
            time = mycursor.fetchall ()
            time=[i[0] for i in time]
            mycursor.execute ("select Headache_name from Headache where u_id='5'")
            name = mycursor.fetchall ()
            name=[i[0] for i in name]
            #scatter plot
            img = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            plt.scatter(time,name,color=['red','green','blue'])
            #Adjusts the subplot(s) to fit in the figure area
            plt.tight_layout()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            #line chart
            plt.clf()
            img1 = io.BytesIO()
            plt.ylabel('Headache Name', fontsize=18)
            plt.xlabel('Time', fontsize=18)
            plt.title('Headache Name vs Time', fontsize=20)
            # plt.barh(time,name, align='center', alpha=0.5, height=0.8)
            plt.plot(time, name, c='xkcd:baby poop green')
            plt.savefig(img1, format='png')
            img1.seek(0)
            plot_url1 = base64.b64encode(img1.getvalue()).decode()
            return render_template('Num_Headache.html',plot_url=plot_url,plot_url1=plot_url1)
        elif selectedValue=='Wokeup':
            #pie_chart
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='Yes' and u_id='5'")
            val = mycursor.fetchall ()
            val=[i[0] for i in val]
            mycursor.execute ("select count(h_id) from Headache where Wokeupwith='No' and u_id='5'")
            count = mycursor.fetchall ()
            count=[i[0] for i in count]
            piechart=[]
            piechart.append(val[0])
            piechart.append(count[0])
            activities = ['Yes','No']
            cols = ['c','m']
            plt.clf()
            plt.pie(piechart,labels=activities,colors=cols,startangle=90,shadow= True,autopct='%1.1f%%')
            plt.title('Woke up with Headache', fontsize=20)
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('wokeup.html',plot_url=plot_url)
        elif selectedValue=='Duration':
            #Bubble_chart
            mycursor.execute ("select Duration from Headache where u_id='5'")
            dur = mycursor.fetchall ()
            dur=[i[0] for i in dur]
            #extracting the integer
            int_dur = [int(x[:-6])*60 for x in dur]
            data_hashmap={}
            data_hashmap={'Mild' : 1 , 'Moderate': 2 , 'Severe': 3}
            mycursor.execute ("select Severity from Headache where u_id='5'")
            data = mycursor.fetchall ()
            data=[i[0] for i in data]
            new_data=[]
            for i in data:
                if i in data_hashmap:
                    new_data.append(data_hashmap[i])
            mycursor.execute ("select Headache_name from Headache where u_id='5'")
            labels = mycursor.fetchall ()
            labels=[i[0] for i in labels]
            plt.clf()
            plt.scatter(labels, new_data, s=int_dur*1000, alpha=0.5,color=['red','green','blue'])
            # plt.tight_layout()
            img = io.BytesIO()
            plt.ylabel('Severity', fontsize=18)
            plt.xlabel('Headache Name', fontsize=18)
            plt.title('Name vs Severity vs Duration', fontsize=20)
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()
            return render_template('Duration.html',plot_url=plot_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #fetching Username and password from database for admin
    mycursor.execute ("select Username,Password from Users where role='admin' and Status='Active'")
    data = mycursor.fetchall ()
    #Storing the username and password fetched into dictionary
    # dict={}
    user_pwd={}
    for row in data:
        user_pwd[row[0]]= row[1]
    #Obtaining the values that the user input
    userName = request.values.get("uname", None)
    userPasswd = request.values.get("passwd", None)
    #checking if the password matches the admin password
    if userName in user_pwd and userPasswd == user_pwd[userName]:
        #Fetching the list of users
        mycursor.execute ("select First_name from Users where role!='admin' and Status='Active'")
        rows = mycursor.fetchall ()
        rows=[i[0] for i in rows]
        return render_template('radio.html', title='CSCI 485 Demonstration', members=rows)
    else:
        # flash('You were not logged in')
        return render_template('login.html')

@app.route('/displayuser', methods=['GET', 'POST'])
def displayuser():
    if request.method == 'POST':
        selectedValue=request.form['patients']
        # return redirect(url_for('click', selectedValue=selectedValue))
        if selectedValue=='John':
            mycursor.execute ("select Headache_name from Headache where u_id='1'")
            rows = mycursor.fetchall ()
            rows=[i[0] for i in rows]
            return render_template('user1.html', title='CSCI 485 Demonstration', name=rows)
        elif selectedValue=='Jonna':
            mycursor.execute ("select Headache_name from Headache where u_id='2'")
            rows = mycursor.fetchall ()
            rows=[i[0] for i in rows]
            return render_template('user2.html', title='CSCI 485 Demonstration', name=rows)
        elif selectedValue=='Kane':
            mycursor.execute ("select Headache_name from Headache where u_id='3'")
            rows = mycursor.fetchall ()
            rows=[i[0] for i in rows]
            return render_template('user3.html', title='CSCI 485 Demonstration', name=rows)
        elif selectedValue=='Jon':
            mycursor.execute ("select Headache_name from Headache where u_id='4'")
            rows = mycursor.fetchall ()
            rows=[i[0] for i in rows]
            return render_template('user4.html', title='CSCI 485 Demonstration', name=rows)
        elif selectedValue=='Jane':
            mycursor.execute ("select Headache_name from Headache where u_id='5'")
            rows = mycursor.fetchall ()
            rows=[i[0] for i in rows]
            return render_template('user5.html', title='CSCI 485 Demonstration', name=rows)

@app.route('/displayjohn', methods=['GET', 'POST'])
def displayjohn():
    if request.method == 'POST':
        selectedValue=request.form['Headache']
        if selectedValue=='Sinus Headache':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='1' and h_id='1'")
            rows = mycursor.fetchall ()
            return render_template('John_Headache_details.html', title='CSCI 485 Demonstration', rows=rows)
        elif selectedValue=='Chatbot':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='1' and h_id='2'")
            rows = mycursor.fetchall ()
            return render_template('John_Headache_details1.html', title='CSCI 485 Demonstration', rows=rows)
        elif selectedValue=='Migraine':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='1' and h_id='3'")
            rows = mycursor.fetchall ()
            return render_template('John_Headache_details2.html', title='CSCI 485 Demonstration', rows=rows)

@app.route('/displayinfo', methods=['GET', 'POST'])
def displayinfo():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='1' and u_id='1'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='1'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayinfo1', methods=['GET', 'POST'])
def displayinfo1():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='2' and u_id='1'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='2'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayinfo2', methods=['GET', 'POST'])
def displayinfo2():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='3' and u_id='1'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='3'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayjonna', methods=['GET', 'POST'])
def displayjonna():
    if request.method == 'POST':
        selectedValue=request.form['Headache']
        if selectedValue=='Stress':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='2' and h_id='4'")
            rows = mycursor.fetchall ()
            return render_template('Jonna_Headache_details.html', title='CSCI 485 Demonstration', rows=rows)
        elif selectedValue=='Tension':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='2' and h_id='5'")
            rows = mycursor.fetchall ()
            return render_template('Jonna_Headache_details1.html', title='CSCI 485 Demonstration', rows=rows)
        elif selectedValue=='Migraine':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='2' and h_id='6'")
            rows = mycursor.fetchall ()
            return render_template('Jonna_Headache_details2.html', title='CSCI 485 Demonstration', rows=rows)

@app.route('/displayinfo3', methods=['GET', 'POST'])
def displayinfo3():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='4' and u_id='2'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='4'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayinfo4', methods=['GET', 'POST'])
def displayinfo4():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='5' and u_id='2'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='5'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayinfo5', methods=['GET', 'POST'])
def displayinfo5():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='6' and u_id='2'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='6'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayjon', methods=['GET', 'POST'])
def displayjon():
    if request.method == 'POST':
        selectedValue=request.form['Headache']
        if selectedValue=='Exams':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='4' and h_id='10'")
            rows = mycursor.fetchall ()
            return render_template('Jon_Headache_details.html', title='CSCI 485 Demonstration', rows=rows)
        elif selectedValue=='AI':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='4' and h_id='11'")
            rows = mycursor.fetchall ()
            return render_template('Jon_Headache_details1.html', title='CSCI 485 Demonstration', rows=rows)
        elif selectedValue=='Migraine':
            mycursor.execute ("select h_id,Wokeupwith,Duration,Severity,Num_times,Facility, M_cycle from Headache where u_id='4' and h_id='12'")
            rows = mycursor.fetchall ()
            return render_template('Jon_Headache_details2.html', title='CSCI 485 Demonstration', rows=rows)

@app.route('/displayinfo6', methods=['GET', 'POST'])
def displayinfo6():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='10' and u_id='4'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='10'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayinfo7', methods=['GET', 'POST'])
def displayinfo7():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='11' and u_id='4'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='11'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displayinfo8', methods=['GET', 'POST'])
def displayinfo8():
    if request.method == 'POST':
        selectedValue=request.form['view']
        if selectedValue=='View Questions and Responses':
            mycursor.execute ("select r_id,m_id,QuestionText,Response_Text from Response where h_id='12' and u_id='4'")
            responses = mycursor.fetchall ()
            return render_template('John_qa.html', title='CSCI 485 Demonstration', responses=responses)
        elif selectedValue=='View Medication Details':
            mycursor.execute ("select m_id,h_id,Medication_name,Pills,Prior_medication_severity from Medication where h_id='12'")
            medication = mycursor.fetchall ()
            return render_template('John_Medication.html', title='CSCI 485 Demonstration', medication=medication)

@app.route('/displaysettings', methods=['GET', 'POST'])
def displaysettings():
    if request.method=='POST':
        mycursor.execute ("select First_name from Users")
        rows = mycursor.fetchall ()
        rows=[i[0] for i in rows]
        return render_template('user_settings.html', title='CSCI 485 Demonstration', members=rows)

@app.route('/user_activity', methods=['GET', 'POST'])
def user_activity():
    global user_name
    if request.method=='POST':
        user_name=request.form['user']
        return render_template('user_activity.html', title='CSCI 485 Demonstration')

@app.route('/status', methods=['GET', 'POST'])
def status():
    if request.method=='POST':
        activity=request.form['Activity']
        if activity=='User status':
            return render_template('user_status.html', title='CSCI 485 Demonstration')
        elif activity=='Access Rights':
            return render_template('access_rights.html', title='CSCI 485 Demonstration')

@app.route('/end', methods=['GET', 'POST'])
def end():
    global user_name
    if request.method=='POST':
        activity=request.form['state']
        if activity=='Activate':
            sql = "UPDATE Users SET status = 'Active' WHERE First_name = '"+user_name+"'"
            mycursor.execute(sql)
            mydb.commit()
        elif activity=='Suspend':
            sql = "UPDATE Users SET status = 'Suspended' WHERE First_name = '"+user_name+"'"
            mycursor.execute(sql)
            mydb.commit()
    mycursor.execute ("select u_id, First_name, Last_name, Gender, Email, Username, Role, Status from Users")
    rows = mycursor.fetchall ()
    # rows=[i[0] for i in rows]
    return render_template('table.html', title='CSCI 485 Demonstration', rows=rows)

@app.route('/finish_access', methods=['GET', 'POST'])
def finish_access():
    global user_name
    if request.method=='POST':
        access=request.form['rights']
        if access=='Admin':
            sql = "UPDATE Users SET Role = 'Admin' WHERE First_name = '"+user_name+"'"
            mycursor.execute(sql)
            mydb.commit()
        elif access=='User':
            sql = "UPDATE Users SET Role = 'User' WHERE First_name = '"+user_name+"'"
            mycursor.execute(sql)
            mydb.commit()
    mycursor.execute ("select u_id, First_name, Last_name, Gender, Email, Username, Role, Status from Users")
    rows = mycursor.fetchall ()
    # rows=[i[0] for i in rows]
    return render_template('table.html', title='CSCI 485 Demonstration', rows=rows)

@app.route('/hello')
def hello_world():
    return 'Hello api.ai (from Flask!)'

@app.route("/", methods=['GET', 'POST'])
def server():

    # get SMS metadata
    msg_from = request.values.get("From", None)
    msg = request.values.get("Body", None)

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = msg

    # get response from API.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    reply="Hello"
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
        # send SMS response back via twilio
        reply=client.messages.create(to=msg_from, from_= account_num, body=response)

    return str(reply)

if __name__ == "__main__":
    app.run(debug=True)

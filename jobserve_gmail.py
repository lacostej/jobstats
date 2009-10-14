# extract information from jobserve emails as stored in my gmail account
# prints it out on the standard output as some sort of CSV format (subject, amount). The subject contains a comma
# author jerome.lacoste@gmail.com
import sys
import imaplib, base64, re
import email

def find_jobs_count(message):
  for line in message.split("\n"):
    m = re.search('.*today contains (.*) job.*', line)
    if m != None:
      if len(m.groups()) == 1:
        return m.group(1)
  return ""


def find_jobs_count_in_data(data):
  for response_part in data:
    if isinstance(response_part, tuple):
      msg = email.message_from_string(response_part[1])
      for part in msg.walk():
        if str(part.get_content_type()) == 'text/plain':
          messagePlainText = str(part.get_payload())
          return find_jobs_count(messagePlainText)
        if str(part.get_content_type()) == 'text/html':
          messageHTML = str(part.get_payload())
  return ""

def print_jobserve_data_as_csv(imap_folder, username, password):

  mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)

  mail.login(username, password)

  n = mail.select(imap_folder)
  if n == 0:
    mail.close()
    return

  typ, data = mail.search(None, 'ALL')

  for mail_id in data[0].split():
#    typ, data = mail.fetch(mail_id, '(RFC822)')
#    print 'Message %s\n%s\n' % (mail_id, data[0][1])
#    mail_from = mail.fetch(mail_id,"(BODY[HEADER.FIELDS (FROM)])")[1][0][1]

    # note the subject as print contains itself a comma, so I am not really printing out proper CSV here...
    subject = mail.fetch(mail_id,"(BODY[HEADER.FIELDS (SUBJECT)])")[1][0][1]
    typ, data = mail.fetch(mail_id, '(RFC822)')
    nb = "0"
    nb = find_jobs_count_in_data(data)
    all = [subject, nb]
    all = [ x.replace("\r", "").replace("\n", "").strip() for x in all] 
    print ",".join(all)
    sys.stdout.flush()

  mail.close()	
  mail.logout()

if __name__ == "__main__":
  if len(sys.argv) < 2:
    print "Usage: " + sys.argv[0] + " username [password]"
    print "Fetches jobserve stats from your gmail jobs folder"

  username = sys.argv[1]
  password = None
  if len(sys.argv) > 2:
    password = sys.argv[2]
  else:
    import getpass
    password = getpass.getpass()

#  print password
  try:
    print_jobserve_data_as_csv("jobs", username, password)
  except KeyboardInterrupt:
    print "Interrupted..."

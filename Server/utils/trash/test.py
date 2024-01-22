import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(subject, message, to_email):
    # Ihre E-Mail-Adresse und das Passwort
    from_email = "noreply.information@theshopmaster.de"
    password = "fPrYRN7MB64HnBsh!eAZ%bf6&TXKk$"

    # Erstellen einer Multipart-Nachricht
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    # Fügen Sie den Nachrichtentext hinzu
    msg.attach(MIMEText(message, 'plain'))

    # Verbindung mit dem Server herstellen und E-Mail senden
    try:
        server = smtplib.SMTP_SSL('webmail.theshopmaster.de', 465) # SMTP Server und Port ändern
        print("Erfolgreich verbunden")
        #server.starttls() # Für eine sichere Verbindung
        server.login(from_email, password)
        print("Erfolgreich eingeloggt")
        server.send_message(msg)
        server.quit()
        print("E-Mail erfolgreich gesendet an", to_email)
    except Exception as e:
        print(f"Fehler beim Senden der E-Mail: {e}")

# Beispiel für das Senden einer E-Mail
send_email("Test Subject", "Dies ist eine Testnachricht.", "schuetzeandreas.1@web.de")

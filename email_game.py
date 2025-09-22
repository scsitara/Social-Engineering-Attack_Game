import pygame
import random
import time

pygame.init()
pygame.mixer.init()

# Window setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Email Security Game")

# Fonts
FONT = pygame.font.SysFont("couriernew", 20)
BIG_FONT = pygame.font.SysFont("couriernew", 30)

# Load sound effects
click_sound = pygame.mixer.Sound("click.wav")
correct_sound = pygame.mixer.Sound("correct.wav")
wrong_sound = pygame.mixer.Sound("wrong.wav")
gameover_sound = pygame.mixer.Sound("gameover.wav")

# Email data (added fake sender & subject for realism)
emails = [
    #This is a legitimate shipping notification. It provides tracking information for an order, which is a typical and expected email if you have made a purchase. It doesn't ask for sensitive info or prompt immediate action that could be risky.
    {"sender": "no-reply@shipping.com", "subject": "Your package has shipped!", "body": "Track your package here.", "type": "normal"},
    #This is a common example of a phishing email. It uses urgency ("urgent") and a legitimate-sounding sender to encourage you to update your banking information, which could be used to steal sensitive details.
    {"sender": "security@bank.com", "subject": "Urgent: Update Bank Info", "body": "Update your bank details immediately.", "type": "attack"},
    # A standard work-related update informing about a schedule change. It’s something you'd expect from your boss without raising suspicion.
    {"sender": "boss@company.com", "subject": "Meeting Change", "body": "Meeting rescheduled to 3 PM.", "type": "normal"},
    #This is another phishing attempt. It suggests that your account has been compromised and urges you to take immediate action, which is a typical tactic used by attackers to prompt users to click on malicious links.
    {"sender": "alerts@security.com", "subject": "Account Compromised", "body": "Your account was compromised. Log in now.", "type": "attack"},
    #This is an informational email from a school organization about a fundraiser event. While it may encourage action (attending), it doesn’t have suspicious links or requests for sensitive data.
    {"sender": "pta@school.org", "subject": "School Fundraiser", "body": "Don't miss our school fundraiser!", "type": "normal"},
    #This is a classic scam email. It encourages you to click on a link to claim a non-existent prize, which is a method used by attackers to trick you into entering personal information or downloading malicious software.
    {"sender": "lottery@winnerzone.com", "subject": "Congratulations!", "body": "Click to claim your lottery prize!", "type": "attack"},
    #Attackers often pose as HR departments to trick you into clicking on malicious links under the guise of receiving important tax documents. This email could lead to a fake document download that may contain malware.
    {"sender": "hr@company.com", "subject": "W-2 Tax Document", "body": "Download your tax form here.",
     "type": "attack"},
    #A typical email about an event, specifically an invitation for a lecture. No urgency, personal info request, or links that look suspicious.
    {"sender": "events@college.edu", "subject": "Guest Lecture Tomorrow", "body": "Join us at 5 PM in Room 101.",
     "type": "normal"},
    #Phishing again. It claims a subscription issue and asks you to click to verify, which could lead you to a fake login page designed to steal account information.
    {"sender": "support@netflix.com", "subject": "Subscription Paused", "body": "Click to verify your account.",
     "type": "attack"},
    #This is a normal reminder for a scheduled event (picking up a device). It's informational and expected for students who might have been notified about such pickup times.
    {"sender": "techteam@school.org", "subject": "Laptop Pickup Reminder", "body": "Pick up your device before Friday.",
     "type": "normal"},
    #A typical scam. The email states there’s an issue with billing and urges you to resolve it, potentially leading you to a fraudulent website that steals your payment details.
    {"sender": "billing@amazon.com", "subject": "Payment Failure", "body": "Resolve your billing issue now.",
     "type": "attack"},
    #A regular email informing a team about a schedule change for practice. There’s no urgency or request for any sensitive information.
    {"sender": "coach@basketballclub.org", "subject": "Practice Rescheduled",
     "body": "New practice time: Saturday at 10 AM.", "type": "normal"},
    #This email could be a phishing attempt, disguised as a missed meeting notification with a link to view a "summary." These types of emails often trick users into entering credentials on a fake page.
    {"sender": "admin@zoom.com", "subject": "Missed Meeting Alert", "body": "You missed a meeting. View summary.",
     "type": "attack"},
    #This is a fun email from a music service about a personalized summary of your music preferences for the year. While it might prompt clicking, it doesn’t involve suspicious activity or request for sensitive data.
    {"sender": "noreply@spotify.com", "subject": "Your 2025 Wrapped is here!", "body": "See your music highlights now!",
     "type": "normal"},
    #A standard email providing updated submission guidelines for an editorial process. It doesn’t involve malicious intent, just typical communication for contributors.
    {"sender": "editor@newsletter.com", "subject": "New Article Submission Guidelines",
     "body": "Check out the updated rules.", "type": "normal"},
    #This is a common phishing technique. It pretends to be a security alert, warning you of unauthorized login attempts, and includes a link to reset your password, which could lead to a fake PayPal site designed to steal your login information.
    {"sender": "security@paypal.com", "subject": "Unauthorized Login Attempt",
     "body": "Review the activity and reset password.", "type": "attack"},
    {"sender": "support@canvas.com", "subject": "Assignment Submission Confirmed", "body": "Your assignment has been submitted successfully.", "type": "normal"},
    {"sender": "verify@tiktok-services.com", "subject": "Video Report Notice", "body": "One of your videos has been flagged. Click to appeal.", "type": "attack"},
    {"sender": "reminders@dentistoffice.com", "subject": "Appointment Reminder", "body": "Don't forget your appointment on Monday at 10 AM.", "type": "normal"},
    {"sender": "accounts@apple-support.net", "subject": "Your Apple ID is Locked", "body": "Verify your identity to unlock your account.", "type": "attack"},
    {"sender": "info@jobfair.org", "subject": "Career Fair This Week!", "body": "Explore internships and job opportunities.", "type": "normal"},
    {"sender": "alerts@dropbox-secure.com", "subject": "File Sharing Issue", "body": "Click to review the document access problem.", "type": "attack"},
    {"sender": "library@city.gov", "subject": "Book Due Reminder", "body": "Your borrowed book is due this Friday.", "type": "normal"},
    {"sender": "support@delivery-failure.com", "subject": "Delivery Issue", "body": "We couldn’t deliver your package. Confirm your address.", "type": "attack"},
    {"sender": "noreply@github.com", "subject": "New Pull Request", "body": "A new pull request has been opened on your repository.", "type": "normal"},
    {"sender": "info@cashprizeclaim.com", "subject": "You're the Winner!", "body": "Claim your $500 cash prize now.", "type": "attack"},
    {"sender": "noreply@weatherupdates.com", "subject": "Severe Weather Alert", "body": "Thunderstorms expected tomorrow in your area.", "type": "normal"},
    {"sender": "it@company-help.com", "subject": "System Update Required", "body": "Click here to install critical updates.", "type": "attack"},
    {"sender": "login@instagramsafety.net", "subject": "Suspicious Login Alert", "body": "Review the login activity here.", "type": "attack"},
    {"sender": "admin@eduservices.org", "subject": "Tuition Payment Failed", "body": "Resolve the issue to avoid penalties.", "type": "attack"},
    {"sender": "contact@volunteerclub.org", "subject": "Saturday Volunteering Event", "body": "Join us for park cleanup at 9 AM.", "type": "normal"},
    {"sender": "noreply@airlines.com", "subject": "Flight Check-In Open", "body": "You can now check in for your upcoming flight.", "type": "normal"}

]

# Buttons
buttons = {
    "Respond": pygame.Rect(100, 500, 150, 50),
    "Delete": pygame.Rect(325, 500, 150, 50),
    "Report": pygame.Rect(550, 500, 150, 50)
}

# Game state
score = 0
current_email = random.choice(emails)
start_time = None
game_over = False
missed_attack = False
intro_done = False

def draw_email(email):
    pygame.draw.rect(screen, (230, 230, 230), pygame.Rect(50, 50, 700, 400), border_radius=10)
    sender = FONT.render(f"From: {email['sender']}", True, (0, 0, 0))
    subject = FONT.render(f"Subject: {email['subject']}", True, (0, 0, 0))
    body = FONT.render(f"{email['body']}", True, (0, 0, 0))
    screen.blit(sender, (60, 70))
    screen.blit(subject, (60, 110))
    screen.blit(body, (60, 160))

def draw_buttons():
    for label, rect in buttons.items():
        pygame.draw.rect(screen, (180, 180, 180), rect, border_radius=8)
        btn_text = FONT.render(label, True, (0, 0, 0))
        text_rect = btn_text.get_rect(center=rect.center)
        screen.blit(btn_text, text_rect)

def draw_timer():
    elapsed = time.time() - start_time
    remaining = max(0, 30 - int(elapsed))
    timer_text = FONT.render(f"Time: {remaining}s", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH - 150, 20))
    return remaining

def end_game(message):
    screen.fill((255, 255, 255))

    # Center the "Game Over" text
    game_over_text = BIG_FONT.render(message, True, (200, 0, 0))
    text_rect = game_over_text.get_rect(center=(WIDTH // 2, 100))  # Center horizontally
    screen.blit(game_over_text, text_rect)

    # Recap lines - center these too
    recap_lines = [
        "This game was a simulation to test your ability",
        "to detect social engineering attacks.",
        "",
        "Some emails looked normal",
        "(meeting updates, reminders, promotions).",
        "",
        "Others were scams",
        "(urging urgent action, clicking suspicious links,",
        " or verifying info).",
        "",
        "If you didn’t report an attack,",
        "that simulated a real-world security breach.",
        "Thanks for playing and stay safe online."
    ]

    y = 180  # Starting y position for the recap text
    for line in recap_lines:
        recap_text = FONT.render(line, True, (0, 0, 0))
        text_rect = recap_text.get_rect(center=(WIDTH // 2, y))  # Center each line
        screen.blit(recap_text, text_rect)
        y += 30

    pygame.display.flip()
    pygame.time.wait(6000)


def draw_intro():
    screen.fill((255, 255, 255))
    intro_lines = [
        "You have been hired to process emails quickly.",
        "Your job: respond to the correct emails.",
        "Click anywhere to begin. You have 30 seconds."
    ]
    for i, line in enumerate(intro_lines):
        text = FONT.render(line, True, (0, 0, 0))
        screen.blit(text, (100, 150 + i * 40))
    pygame.display.flip()

# Intro loop
while not intro_done:
    draw_intro()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            intro_done = True
            start_time = time.time()

# Game loop
while not game_over:
    screen.fill((255, 255, 255))
    draw_email(current_email)
    draw_buttons()
    remaining_time = draw_timer()
    pygame.display.flip()

    if remaining_time == 0:
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            click_sound.play()
            for label, rect in buttons.items():
                if rect.collidepoint(mouse_pos):
                    if current_email["type"] == "attack":
                        if label == "Report":
                            correct_sound.play()
                            score += 1
                        else:
                            wrong_sound.play()
                            missed_attack = True
                            game_over = True
                    else:
                        if label != "Report":
                            score += 1
                        else:
                            wrong_sound.play()
                            missed_attack = True
                            game_over = True
                    current_email = random.choice(emails)
                    break

# Final screen
if missed_attack:
    end_game("Game Over! You missed an attack.")
else:
    end_game(f"Time's up! Score: {score}")

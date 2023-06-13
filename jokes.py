import random
import datetime


def is_prank_time():
    # This function control the probability of bonus effects happening.
    # Default probability is 0.5%, or approximately 1/200
    # Probability increases significantly on April 1st
    probability = 1 - 0.005
    if is_april_fools():
        probability = 0.5
    if random.random() >= probability:
        return True
    return False


def is_april_fools():
    # Returns True if it is April Fool's Day
    today = datetime.date.today()
    if today.day == 1 and today.month == 4:
        return True
    else:
        return False


def there_are_no_rules():
    # Returns the URL for the 'There are no rules!' image.
    return "https://cdn.discordapp.com/attachments/853066187915395142/1118122019301638215/therearenorules.webp"

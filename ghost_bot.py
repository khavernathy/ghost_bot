import discord
from discord.ext import commands
import numpy as np
from levenshtein import levenshtein as lev

# to add to your discord channel,
# https://discord.com/oauth2/authorize?client_id=769805113266798593&scope=bot

evidence = ['emf', 'box', 'prints', 'orbs', 'writing', 'freeze', 'dots']
#             0     1       2         3       4         5         6
# ghosts can be ID'd by which evidence pertains to them.
def e2i(e):
    return evidence.index(e)
ghosts = dict({'spirit': [e2i("emf"), e2i("box"), e2i("writing")],
               'wraith': [e2i("emf"), e2i("box"), e2i("dots")],
               'phantom': [e2i("box"), e2i("prints"), e2i("dots")],
               'poltergeist': [e2i("box"), e2i("prints"), e2i("writing")],
               'banshee': [e2i("prints"), e2i("orbs"), e2i("dots")],
               'jinn': [e2i("emf"), e2i("prints"), e2i("freeze")],
               'mare': [e2i("box"), e2i("orbs"), e2i("writing")],
               'revenant': [e2i("orbs"), e2i("writing"), e2i("freeze")],
               'shade': [e2i("emf"), e2i("writing"), e2i("freeze")],
               'demon': [e2i("prints"), e2i("writing"), e2i("freeze")],
               'yurei': [e2i("orbs"), e2i("freeze"), e2i("dots")],
               'yokai': [e2i("box"), e2i("orbs"), e2i("dots")],
               'hantu': [e2i("prints"), e2i("orbs"), e2i("freeze")],
               'oni': [e2i("emf"), e2i("freeze"), e2i("dots")],
               'goryo': [e2i("emf"), e2i("prints"), e2i("dots")],
               'myling': [e2i("emf"), e2i("prints"), e2i("writing")],
               })

ghost_desc = dict({
    'spirit': 'A spirit is the most common Ghost you will come across however it is still very powerful and dangerous. They are usually discovered at one of their hunting grounds after an unexplained death.'
              '\n\n:muscle: Strengths: Nothing'
              '\n:no_entry: Weaknesses: Using Smudge Sticks on a Spirit will stop it attacking for a long period of time.',
    'wraith': 'A wraith is one of the most dangerous Ghosts you will find. It is also the only known Ghost that has the abililty of flight and has sometimes been known to travel through walls.'
              '\n\n:muscle: Strengths: Wraiths almost never touch the ground meaning it cant be tracked by footsteps.'
              '\n:no_entry: Weaknesses: Wraiths have a toxic reaction to Salt.',
    'phantom': 'A Phantom is a Ghost that can possess the living, most commonly summoned by a Ouija board. It also induces fear into those around it.'
               '\n\n:muscle: Strengths: Looking at a phantom will considerably drop your sanity.'
               '\n:no_entry: Weaknesses: Taking a photo of the Phantom will make it temporarily disappear.',
    'poltergeist': 'One of the most famous Ghosts, a Poltergeist, also know as a noisy ghost can manipulate objects around it to spread fear into its victims.'
                   '\n\n:muscle: Strengths: A Poltergeist can throw huge amounts of objects at once.'
                   '\n:no_entry: Weaknesses: A Poltergeist is almost ineffective in an empty room.',
    'banshee': 'A Banshee is a natural hunter and will attack anything. It has been known to stalk its prey one at a time until making its kill.'
               '\n\n:muscle: Strengths: A Banshee will only target one person at a time.'
               '\n:no_entry: Weaknesses: Banshees fear the crucifix and will be less aggressive when near one.',
    'jinn': 'A Jinn is a territorial Ghost that will attack when threatened. It has also been known to be able to travel at significant speed.'
            '\n\n:muscle: Strengths: A Jinn will travel at a faster speed if its victim is far away.'
            '\n:no_entry: Weaknesses: Turning off the locations power source will prevent the Jinn from using its ability.',
    'mare': 'A Mare is the source of all nightmares, making it most powerful in the dark.'
            '\n\n:muscle: Strengths: A Mare will have an increased chance to attack in the dark.'
            '\n:no_entry: Weaknesses: Turning the lights on around the Mare will lower its chance to attack',
    'revenant': 'A Revenant is a slow but violent Ghost that will attack indiscriminately. It has been rumored to travel at a significantly high speed when hunting.'
                '\n\n:muscle: Strengths: A Revenant will travel at a significantly faster speed when hunting a vicitm.'
                '\n:no_entry: Weaknesses: Hiding from the Revenant will cause it to move very slowly.',
    'shade': 'A Shade is known to be a shy Ghost. There is evidence that a Shade will stop all paranormal activity if there are multiple people nearby.'
             '\n\n:muscle: Strengths: Being shy means the Ghost will be harder to find.'
             '\n:no_entry: Weaknesses: The Ghost will not enter hunting mode if there is multiple people nearby.',
    'demon': 'A Demon is one of the worst Ghosts you can encounter. It has been known to attack without a reason.'
             '\n\n:muscle: Strengths: Demons will attack more often than any other Ghost.'
             '\n:no_entry: Weaknesses: Asking a Demon successful questions on the Ouija Board wont lower the users sanity.',
    'yurei': 'A Yurei is a Ghost that has returned to the physical world, usually for the purpose of revenge or hatred.'
             '\n\n:muscle: Strengths: Yureis have been known to have a stronger effect of peoples sanity.'
             '\n:no_entry: Weaknesses: Smudging the Yureis room will cause it to not wander around the location for a long time.',
    'yokai': 'A common type of ghost that is attracted to human voices. They can usually be found haunting family homes.'
             '\n\n:muscle: Strengths: Talking near a Yokai will anger it and cause it to attack more often.'
             '\n:no_entry: Weaknesses: While hunting, it can only hear voices close to it.',
    'hantu': 'A rare ghost that can be found in hot climates. They are known to attack more often in cold weather.'
             '\n\n:muscle: Strengths: Hantu moves faster in colder areas.'
             '\n:no_entry: Weaknesses: Hantu moves slower in warmer areas.',
    'oni': 'Onis are a cousin to the Demon and possess extreme strength.There have been rumors that they become more active around their prey.'
           '\n\n:muscle: Strengths: Onis are more active when people are nearby and have been seen moving objects at great speed.'
           '\n:no_entry: Weaknesses: Being more active will make the Oni easier to find and identify.',
    'goryo': 'When a Goryo passes through a DOTS Projector, using a video camera is the only way to see it.'
           '\n\n:muscle: Strengths: A Goryo will usually only show itself on camera if there are no people nearby.'
           '\n:no_entry: Weaknesses: They are rarely seen far from their place of death.',
    'myling': 'A Myling is a very vocal and active ghost. They are rumoured to be quiet when hunting their prey.'
           '\n\n:muscle: Strengths: A Myling is known to be quieter when hunting.'
           '\n:no_entry: Weaknesses: Mylings more frequently make paranormal sounds.',
    })


# synonym function to translate user input smartly
def syn(x):
    if len(x) > 2:
        # string (including literal) match
        for evi in evidence:
            if lev(x.lower(), evi):
                return evi
        # alias match. Order matters because edge cases suck
        aliases = dict({'spirit': 'box',
                        'radio': 'box',
                        'finger': 'prints',
                        'book': 'writing',
                        'temp': 'freeze',
                        'freezing': 'freeze',
                        'projector': 'dots',
                        })
        for key in aliases:
            if lev(x.lower(), key):
                return aliases[key]
    # if there's no match we return false
    return False


# same but for ghost-names
def syn_ghost(x):
    for ghost in ghosts:
        if lev(x.lower(), ghost):
            return ghost
    # if there's no match we return false
    return False


# get a string that shows the clues true for a given ghost with respect to user input clues
def ghost_clues_string(ghost, clues, blanks=False):
    inds = ghosts[ghost]
    givens = []
    for given in clues:
        givens.append(evidence.index(given))
    if blanks:
        m1 = ':grey_question:'
        m2 = ':grey_question:'
        m3 = ':grey_question:'
    else:
        m1 = ':green_circle: ' if inds[0] in givens else ':red_circle: '
        m2 = ':green_circle: ' if inds[1] in givens else ':red_circle: '
        m3 = ':green_circle: ' if inds[2] in givens else ':red_circle: '
    return m1 + evidence[inds[0]] + ", " + m2 + evidence[inds[1]] + ", " + m3 + evidence[inds[2]]


def help_text():
    return str('\nExamples:'
               '\n\n**!ghost emf,box**'
               '\n**!ghost prints,orbs**'
               '\n**!ghost writing,freeze,orbs**'
               '\n**!ginfo poltergeist**'
               '\n**!ginfo wraith**'
               '\n**!rand 6**'
               '\n\nNote, **!info** is now **!ginfo**')


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("The bot is rdy")


@bot.command()
async def halp(ctx):
    await ctx.send(help_text())


@bot.command()
async def hello(ctx):
    await ctx.send("Hello")


# give me a random int from 1 -> n
@bot.command(pass_context=True)
async def rand(ctx, val):
    if isinstance(int(val), int):
        val = int(val)
        await ctx.send(':game_die: ' + str(int(np.ceil(np.random.random() * val))))
    else:
        await ctx.send("that's not an integer")


# deduce which ghosties could be to blame based on evidence found
@bot.command(pass_context=True)
async def ghost(ctx, *, msg=None):

    if msg is None:
        await ctx.send("You didn't enter any ghost clues.")
        await ctx.send(help_text())

    # get match indices
    matches = []
    # split input args by comma
    input_clues = msg.split(",")
    # remove whitespace and empty listings
    input_clues = [clue.replace(" ", "") for clue in input_clues if clue != ""]

    # input validation
    if len(input_clues) > 3:
        await ctx.send('No more than 3 clues allowed.')
        await ctx.send(help_text())
        return
    # find synonyms and aliases
    filtered_clues = []
    for i, clue in enumerate(input_clues):
        filtered_clues.append(syn(clue))
    # if any bad entires, show and exit
    if False in filtered_clues:
        await ctx.send("I don't understand this hint: " + input_clues[filtered_clues.index(False)])
        await ctx.send(help_text())
        return

    # find clue-matches for the filtered (correct) clues
    for clue in filtered_clues:
        for i, evi in enumerate(evidence):
            if evi == clue:
                matches.append(i)

    print("user input: ", input_clues)
    print("filtered to: ", filtered_clues)

    # check which ghosts could match
    if len(matches) > 0:
        ghost_matches = []
        for ghost in ghosts:
            ghost_clues = ghosts[ghost]
            if all(item in ghost_clues for item in matches):
                ghost_matches.append(ghost)

        print("ghost_matches: ", ghost_matches)
        if len(ghost_matches) == 0:
            await ctx.send("No ghost matches those clues.")
            await ctx.send(help_text())
            return
        out_str = ""
        for candidate in ghost_matches:
            out_str = out_str + ":ghost: `" + candidate + "`: " + ghost_clues_string(candidate, filtered_clues) + "\n"
        await ctx.send(out_str)

        # finally, if we narrowed it down, show ghost info
        if len(ghost_matches) == 1:
            await ctx.send(ghost_desc[candidate])

    else:
        await ctx.send(help_text())


# get information about a specific ghost-type
@bot.command(pass_context=True)
async def ginfo(ctx, msg=None):
    if msg is None:
        await ctx.send("You didn't enter a ghost name.")
        await ctx.send(help_text())

    ghostname = syn_ghost(msg)
    if not ghostname:
        await ctx.send("I don't understand the ghost you typed: " + msg)
        await ctx.send(help_text())
        return
    else:
        await ctx.send(':ghost: `' + ghostname + '`: ' +
                       ghost_clues_string(ghostname, [], blanks=True) + '\n' +
                       ghost_desc[ghostname])


# run the bot using super special secret token
bot.run(str(
    np.genfromtxt('TOKEN', dtype='str')
))

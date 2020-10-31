import discord
from discord.ext import commands
import numpy as np
from levenshtein import levenshtein as lev

# to add to your discord channel,
# https://discord.com/oauth2/authorize?client_id=769805113266798593&scope=bot

evidence = ['emf', 'box', 'prints', 'orbs', 'writing', 'freeze']
ghosts = dict({'spirit': [1, 2, 4],
               'wraith': [1, 2, 5],
               'phantom': [0, 3, 5],
               'poltergeist': [1, 2, 3],
               'banshee': [0, 2, 5],
               'jinn': [0, 1, 3],
               'mare': [1, 3, 5],
               'revenant': [0, 2, 4],
               'shade': [0, 3, 4],
               'demon': [1, 4, 5],
               'yurei': [3, 4, 5],
               'oni': [0, 1, 4]
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
    'demon': 'A Demon is one of the worst Ghosts you can encounter. It has been known to attach without a reason.'
             '\n\n:muscle: Strengths: Demons will attack more often than any other Ghost.'
             '\n:no_entry: Weaknesses: Asking a Demon successful questions on the Ouija Board wont lower the users sanity.',
    'yurei': 'A Yurei is a Ghost that has returned to the physical world, usually for the purpose of revenge or hatred.'
             '\n\n:muscle: Strengths: Yureis have been known to have a stronger effect of peoples sanity.'
             '\n:no_entry: Weaknesses: Smudging the Yureis room will cause it to not wander around the location for a long time.',
    'oni': 'Onis are a cousin to the Demon and possess extreme strength.There have been rumors that they become more active around their prey.'
           '\n\n:muscle: Strengths: Onis are more active when people are nearby and have been seen moving objects at great speed.'
           '\n:no_entry: Weaknesses: Being more active will make the Oni easier to find and identify.'
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
                        })
        for key in aliases:
            if lev(x.lower(), key):
                return aliases[key]
    return x


# same but for ghost-names
def syn_ghost(x):
    for ghost in ghosts:
        if lev(x.lower(), ghost):
            return ghost
    return x


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


bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("The bot is rdy")


@bot.command()
async def halp(ctx):
    await ctx.send("Hey spookboi. Use me like this:\n !ghost emf,freeze,orbs")


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
        await ctx.send('u didnt give me an integer binch')


# deduce which ghosties could be to blame based on evidence found
@bot.command(pass_context=True)
async def ghost(ctx, msg):
    # get match indices
    matches = []
    # split input args by comma
    clues = msg.split(",")
    print("user input: ", clues)
    # input validation
    if any('' in clues for item in clues):
        await ctx.send('Dont use spaces between the commas.')
        return
    elif len(clues) > 3:
        await ctx.send('No more than three clues allowed.')
    # find synonyms and aliases
    for i,clue in enumerate(clues):
        clues[i] = syn(clue)
    # show resultant clues to user first
    await ctx.send(clues)

    # find matches
    for clue in clues:
        clue = syn(clue) # get synonyms
        for i,evi in enumerate(evidence):
            if evi == clue:
                matches.append(i)

    # check which ghosts could match
    if len(matches) > 0:
        ghost_matches = []
        for ghost in ghosts:
            ghost_clues = ghosts[ghost]
            if all(item in ghost_clues for item in matches):
                ghost_matches.append(ghost)

        #await ctx.send(clues)
        out_str = ""
        for candidate in ghost_matches:
            out_str = out_str + ":ghost: `" + candidate + "`: " + ghost_clues_string(candidate, clues) + "\n"
        await ctx.send(out_str)

        # finally, if we narrowed it down, show ghost info
        if len(ghost_matches) == 1:
            await ctx.send(ghost_desc[candidate])

    else:
        await ctx.send('I dont understand u. Here i halp. Use like dis:'
                       '\n\n**!ghost emf,box,prints,orbs,writing,freeze**'
                       '\n\n**!info poltergeist**'
                       '\n\n**!rand 6**'
                       '\n\nRemember, no spaces between clues. :ghost:')


# get information about a specific ghost-type
@bot.command(pass_context=True)
async def info(ctx, msg):
    ghostname = syn_ghost(msg)
    await ctx.send(':ghost: `' + ghostname + '`: ' +
                   ghost_clues_string(ghostname, [], blanks=True) + '\n' +
                   ghost_desc[ghostname])


# run the bot using super special secret token
bot.run(str(
    np.genfromtxt('TOKEN', dtype='str')
))
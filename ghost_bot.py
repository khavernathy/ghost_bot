import discord
from discord.ext import commands
import numpy as np

evidence = ['emf', 'box', 'prints', 'orbs', 'writing', 'freeze']
ghosts = dict({'spirit': [1,2,4],
    'wraith': [1,2,5],
    'phantom': [0,3,5],
    'poltergeist': [1,2,3],
    'banshee': [0,2,5],
    'jinn': [0,1,3],
    'mare': [1,3,5],
    'revenant': [0,2,4],
    'shade': [0,3,4],
    'demon': [1,4,5],
    'yurei': [3,4,5],
    'oni': [0,1,4]})

ghost_desc = dict({
    'spirit': 'A spirit is the most common Ghost you will come across however it is still very powerful and dangerous. They are usually discovered at one of their hunting grounds after an unexplained death.\nStrenghts: Nothing\nWeaknesses: Using Smudge Sticks on a Spirit will stop it attacking for a long period of time.',
    'wraith': 'A wraith is one of the most dangerous Ghosts you will find. It is also the only known Ghost that has the abililty of flight and has sometimes been known to travel through walls. Strengths: Wraiths almost never touch the ground meaning it cant be tracked by footsteps.\nWeaknesses: Wraiths have a toxic reaction to Salt.',
    'phantom': 'A Phantom is a Ghost that can possess the living, most commonly summoned by a Ouija board. It also induces fear into those around it.\nStrenghts: Looking at a phantom will considerably drop your sanity.\nWeaknesses: Taking a photo of the Phantom will make it temporarily disappear.',
    'poltergeist': 'One of the most famous Ghosts, a Poltergeist, alsso know as a noisy ghost can manipulate objects around it to spread fear into its victims.\nStrenghts: A Poltergeist can throw huge amounts of objects at once.\nWeaknesses: A Poltergeist is almost ineffective in an empty room.',
    'banshee': 'A Banshee is a natural hunter and will attack anything. It has been known to stalk its prey one at a time until making its kill.\nStrengths: A Banshee will only target one person at a time.\nWeaknesses: Banshees fear the crucifix and will be less aggressive when near one.',
    'jinn': 'A Jinn is a territorial Ghost that will attack when threatened. It has also been known to be able to travel at significant speed.\nStrengths: A Jinn will travel at a faster speed if its victim is far away.\nWeaknesses: Turning off the locations power source will prevent the Jinn from using its ability.',
    'mare': 'A Mare is the source of all nightmares, making it most powerful in the dark.\nStrengths: A Mare will have an increased chance to attack in the dark.\nWeaknesses: Turning the lights on around the Mare will lower its chance to attack',
    'revenant': 'A Revenant is a slow but violent Ghost that will attack indiscriminately. It has been rumored to travel at a significantly high speed when hunting.\nStrengths: A Revenant will travel at a significantly faster speed when hunting a vicitm.\nWeaknesses: Hiding from the Revenant will cause it to move very slowly.',
    'shade': 'A Shade is known to be a shy Ghost. There is evidence that a Shade will stop all paranormal activity if there are multiple people nearby.\nStrenghts: Being shy means the Ghost will be harder to find.\nWeaknesses: The Ghost will not enter hunting mode if there is multiple people nearby.',
    'demon': 'A Demon is one of the worst Ghosts you can encounter. It has been known to attach without a reason.\nStrenghts: Demons will attack more often than any other Ghost.\nWeaknesses: Asking a Demon successful questions on the Ouija Board wont lower the users sanity.',
    'yurei': 'A Yurei is a Ghost that has returned to the physical world, usually for the purpose of revenge or hatred.\nStrengths: Yureis have been known to have a stronger effect of peoples sanity.\nWeaknesses: Smudging the Yureis room will cause it to not wander around the location for a long time.',
    'oni': 'Onis are a cousin to the Demon and possess extreme strength.There have been rumors that they become more active around their prey.\nStrengths: Onis are more active when people are nearby and have been seen moving objects at great speed.\nWeaknesses: Being more active will make the Oni easier to find and identify.'
    })

def ghost_clues_string(ghost):
    i = ghosts[ghost]
    return evidence[i[0]] + ", " + evidence[i[1]] + ", " + evidence[i[2]]

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

@bot.command()
async def rand(ctx):
    await ctx.send(str(np.random.random()))

@bot.command(pass_context=True)
async def ghost(ctx, msg):
    # get match indices
    matches = []
    clues = msg.split(",")
    for clue in clues:
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
        for candidate in ghost_matches:
            await ctx.send('`' + candidate + ": " + ghost_clues_string(candidate) + '`')
            await ctx.send(ghost_desc[candidate])

    else:
        await ctx.send('I dont understand u. Here i halp. Use like dis:\n**!ghost emf,box,prints,orbs,writing,freeze**')



bot.run('NzY5ODA1MTEzMjY2Nzk4NTkz.X5UW4Q.U8h2xBDqWXo4oOehn4ZM6szwIPQ')


const MOVIES = [
  { title: "Jaws", reviews: [
    "A slow-building horror that made an entire generation afraid of open water.",
    "Small beach town officials would rather protect summer tourism than admit a threat lurks offshore.",
    "Three unlikely allies — a lawman, a scientist, and a grizzled seafarer — team up to hunt something enormous.",
    "That two-note theme still makes people's stomachs drop before anything even happens on screen.",
    "A mechanical shark that barely worked on set somehow became one of cinema's most terrifying villains.",
    "“You’re gonna need a bigger boat” has become one of the most quoted lines in movie history."
  ], summary: "A giant great white shark terrorizes the beach town of Amity Island. The local police chief, a marine biologist, and a grizzled shark hunter set out on a boat to track and kill it before it can claim more victims." },

  { title: "The Matrix", reviews: [
    "A film that convinced a generation to question whether reality is actually real.",
    "A mysterious message tells the hero to follow the white rabbit.",
    "A quiet computer programmer is offered a choice between two pills — and his whole world changes.",
    "Bullet-time photography made its slow-motion dodge sequence instantly iconic.",
    "Leather trench coats, sunglasses indoors, and gravity-defying kung fu define its visual style.",
    "Its rebel crew searches for 'the One' destined to free humanity from a simulated prison."
  ], summary: "A hacker named Neo discovers that the world he knows is a simulated reality called the Matrix, built to keep humans docile while machines harvest their bodies for energy. Guided by Morpheus and Trinity, he trains to fight back against the machines controlling it." },

  { title: "Titanic", reviews: [
    "A sweeping romance set against one of history's most famous disasters.",
    "Two people from opposite ends of the social ladder fall for each other during a fateful voyage.",
    "A young woman contemplating jumping is talked down by a free-spirited artist.",
    "There's a debate that has raged for decades about whether both leads could have fit on that floating door.",
    "An elderly survivor recounts the story decades later to treasure hunters searching for a lost necklace.",
    "The ship was billed as unsinkable, which — as any student of irony knows — never ends well."
  ], summary: "Aboard the doomed ocean liner's maiden voyage in 1912, a wealthy young woman and a penniless artist fall in love. Their romance is cut short when the ship strikes an iceberg and sinks, and only one of them survives." },

  { title: "Inception", reviews: [
    "A heist movie that takes place almost entirely inside people's heads.",
    "A team of specialists steals secrets by entering their targets' dreams.",
    "This time, the job isn't to steal an idea but to plant one instead.",
    "A spinning top left teetering on a tabletop sparked years of ending debates.",
    "Dreams within dreams within dreams, each one running on a different clock than the last.",
    "A guilt-ridden extractor is haunted by the memory of his dead wife every time he goes under."
  ], summary: "A skilled thief who steals secrets from people's subconscious through shared dreams is offered a chance to have his criminal record erased if he can perform 'inception' — planting an idea in a target's mind rather than stealing one. As the job descends through nested dream layers, he must also confront the guilt over his wife's death." },

  { title: "Parasite", reviews: [
    "A darkly funny class satire that swerves into something much more unsettling.",
    "A struggling family cons their way into working for a wealthy household, one job at a time.",
    "A hidden space beneath a beautiful home holds a secret nobody in the family expected.",
    "A sudden rainstorm reveals just how differently rich and poor experience the same city.",
    "It became the first non-English-language film to win the Best Picture Oscar.",
    "A birthday party in the backyard turns into total chaos in its final act."
  ], summary: "A poor family schemes their way into becoming employees of a wealthy household by posing as unrelated, highly qualified strangers. When they discover a shocking secret hidden in the house's basement, their carefully constructed deception spirals into violence." },

  { title: "The Godfather", reviews: [
    "A slow, operatic story about family, loyalty, and the price of power.",
    "A patriarch's youngest, most reluctant son is eventually pulled into the family business.",
    "A wedding at the start brings the whole family together before things start to unravel.",
    "A horse's head left in someone's bed sends an unmistakable message.",
    "“I'm gonna make him an offer he can't refuse” is one of the most imitated lines ever written.",
    "By the end, the once-reluctant son has fully become the very thing he tried to avoid."
  ], summary: "The aging patriarch of a powerful Italian-American crime family gradually hands control to his youngest son, who reluctantly becomes drawn into the family's violent business. Over time, the son transforms from a war hero trying to stay out of the mafia into its ruthless new leader." },

  { title: "Jurassic Park", reviews: [
    "A cautionary tale about scientists getting a little too excited about what they can do.",
    "A billionaire invites a small group of experts to preview his new island theme park.",
    "The attractions turn out to be very much alive, and considerably larger than expected.",
    "A glass of water rippling on a dashboard signals something huge is approaching.",
    "Its groundbreaking visual effects made prehistoric creatures look genuinely real on screen for the first time.",
    "A boy obsessed with dinosaurs gets far more than he bargained for once the power goes out."
  ], summary: "A billionaire opens a theme park featuring cloned dinosaurs on a remote island. When the security systems fail during a storm, the dinosaurs escape their enclosures, and the visiting scientists and the owner's grandchildren must survive the night." },

  { title: "Get Out", reviews: [
    "A horror-comedy that doubles as a sharp piece of social commentary.",
    "A young man is nervous about meeting his girlfriend's parents for the first time.",
    "The family's overly friendly hospitality starts to feel more like a performance.",
    "A hypnotic teacup and spoon send someone somewhere they call 'the sunken place.'",
    "A garden party full of guests behaving strangely raises every possible red flag.",
    "The family's household staff seem to be hiding something behind their unsettling smiles."
  ], summary: "A Black man visiting his white girlfriend's family estate for the weekend discovers the family's hospitality masks a horrifying secret operation targeting Black visitors. He must escape before he becomes their next victim." },

  { title: "La La Land", reviews: [
    "A modern musical love letter to the dreamers who chase impossible careers.",
    "Two strangers keep running into each other around the same sprawling city.",
    "An aspiring actress and a jazz purist fall for each other while chasing separate dreams.",
    "A stretch of freeway traffic bursts into full song-and-dance right at the start.",
    "Its bittersweet ending imagines an entire alternate life the couple never got to live.",
    "Its planetarium dance sequence has the two leads literally floating among the stars."
  ], summary: "An aspiring actress and a dedicated jazz pianist fall in love while pursuing their creative dreams in Los Angeles. As their careers pull them in different directions, their romance is tested, and the film closes with a bittersweet vision of the life they might have shared." },

  { title: "Toy Story", reviews: [
    "The first fully computer-animated feature film ever made.",
    "A beloved toy's world is upended when a flashy new arrival steals his owner's attention.",
    "The new arrival doesn't even realize he's a toy at first.",
    "A rescue mission takes the pair through a terrifying neighbor's yard full of mutant toys.",
    "“To infinity and beyond” became a catchphrase for an entire generation of kids.",
    "Its heroes are a cowboy doll and a space ranger action figure who must learn to work together."
  ], summary: "A pull-string cowboy doll named Woody feels threatened when his owner receives a flashy space ranger toy named Buzz Lightyear. After a series of mishaps strands them away from home, the two rivals must learn to cooperate to make it back before moving day." },

  { title: "The Dark Knight", reviews: [
    "A crime saga that reinvented what a superhero movie could feel like.",
    "A city's vigilante protector faces an anarchist who has no interest in money or power.",
    "A district attorney's rise and fall becomes just as important as the hero's own arc.",
    "A ferry standoff forces two boatloads of strangers into an impossible moral choice.",
    "Its late star's unsettling, Oscar-winning performance became the film's most talked-about element.",
    "A vigilante in a bat costume faces a chaos-loving clown with no clear motive at all."
  ], summary: "Batman, along with police lieutenant Jim Gordon and district attorney Harvey Dent, sets out to dismantle organized crime in Gotham City, only to be confronted by the Joker, a criminal mastermind who wants to prove that anyone can be pushed to moral collapse." },

  { title: "Pulp Fiction", reviews: [
    "A nonlinear crime story told out of order, stitched together from overlapping vignettes.",
    "Two hitmen have a long, meandering conversation about fast food on their way to a job.",
    "A boxer double-crosses a crime boss he was supposed to lose a fight for.",
    "A briefcase with mysterious glowing contents is never actually explained to the audience.",
    "A dance contest at a retro diner turns into one of its most memorable scenes.",
    "A gangster's wife accidentally overdoses after mistaking heroin for cocaine at a dinner date."
  ], summary: "The film weaves together several interconnected stories in the Los Angeles criminal underworld: two philosophical hitmen, a boxer who double-crosses his boss, and a gangster's wife who has a dangerous night out, all told out of chronological order." },

  { title: "Forrest Gump", reviews: [
    "A gentle, decades-spanning story told from the perspective of an unlikely witness to history.",
    "A man with a low IQ but a good heart recounts his improbable life to strangers at a bus stop.",
    "He accidentally stumbles into major historical events throughout the 1960s and 70s.",
    "A feather drifting on the wind bookends the whole story.",
    "“Life is like a box of chocolates” became one of the most quoted lines in movie history.",
    "He spends years running back and forth across the country for no particular reason at all."
  ], summary: "A kind-hearted, slow-witted man from Alabama recounts his extraordinary life, which sees him unwittingly present at pivotal moments in American history, all while pining for his childhood friend Jenny." },

  { title: "The Shawshank Redemption", reviews: [
    "A quiet drama about patience, friendship, and holding onto hope in the darkest circumstances.",
    "A wrongly convicted banker adjusts to a brutal new life inside prison walls.",
    "He strikes up an unlikely friendship with a man who can get things from outside the walls.",
    "A rock hammer, hidden inside a hollowed-out book, turns out to matter more than anyone realizes.",
    "A tunnel dug slowly over two decades ends in a dramatic escape through a sewage pipe.",
    "He's finally reunited with his old friend on a beach in Mexico at the very end."
  ], summary: "A banker wrongly convicted of murdering his wife spends nearly two decades in Shawshank prison, forming a deep friendship with a fellow inmate and quietly plotting an elaborate escape that pays off after almost twenty years." },

  { title: "Alien", reviews: [
    "A slow-burn sci-fi horror set entirely in the isolation of deep space.",
    "A commercial spaceship crew answers a distress signal they probably should have ignored.",
    "A crew member's routine encounter with a strange egg goes very wrong, very fast.",
    "One dinner scene turns into an infamous, blood-soaked surprise.",
    "Its warrant officer becomes one of the genre's first great female action heroes.",
    "A synthetic crew member turns out to have a very different set of priorities than the humans."
  ], summary: "The crew of a commercial towing spaceship investigates a distress signal and unknowingly bring aboard a deadly alien organism that begins hunting them down one by one, leaving the ship's officer to fight for survival." },

  { title: "Back to the Future", reviews: [
    "A time-travel comedy powered by a modified sports car.",
    "A teenager accidentally travels decades into the past thanks to his eccentric scientist friend.",
    "He accidentally interferes with how his own parents first met.",
    "A lightning strike at a clock tower becomes crucial to getting back home.",
    "A modified car needs to hit exactly eighty-eight miles per hour to work its magic.",
    "He has to make sure his awkward teenage father actually asks his mother to a dance."
  ], summary: "A teenager is accidentally sent 30 years into the past in a time-traveling car built by his scientist friend. He must make sure his future parents fall in love as originally intended, all while trying to find a way back to his own time." },

  { title: "Gladiator", reviews: [
    "A sweeping historical epic about revenge, honor, and the price of power in ancient Rome.",
    "A celebrated general is betrayed by a jealous emperor's son and loses everything.",
    "Stripped of his rank, he's sold into slavery and forced to fight for entertainment.",
    "“Are you not entertained?” became one of its most quoted lines.",
    "A reunion with his family is only possible in his imagination, in fields of wheat.",
    "He rises through the ranks of gladiatorial combat with the goal of confronting the emperor himself in the Colosseum."
  ], summary: "A betrayed Roman general is enslaved and forced into gladiatorial combat after the corrupt new emperor murders his family. He rises through the ranks of the arena, ultimately facing the emperor himself in the Colosseum to avenge his loved ones." },

  { title: "The Sixth Sense", reviews: [
    "A quiet supernatural drama built around one of cinema's most famous twist endings.",
    "A troubled child psychologist tries to help a young boy who claims to see disturbing things.",
    "The boy whispers that he sees dead people, and he means it literally.",
    "A birthday party scene reveals a truth about a woman that changes everything the audience thought they knew.",
    "A cold breath and dropping temperature signal whenever something isn't quite right nearby.",
    "The therapist eventually realizes he's been dead the entire film, unaware his own case ended in tragedy."
  ], summary: "A child psychologist tries to help a troubled young boy who claims he can see and communicate with the dead. Over the course of the film, the psychologist slowly realizes that he himself has been dead the whole time, killed by a former patient before the story even began." },

  { title: "Fight Club", reviews: [
    "A nihilistic drama about masculinity, consumerism, and one man's spiraling identity crisis.",
    "An insomniac office worker starts attending support groups just to feel something real.",
    "A chance meeting with a charismatic soap salesman changes the course of his life.",
    "Bare-knuckle brawls in a bar basement quietly grow into something much bigger.",
    "Its twist reveals that two of its main characters have been the same person all along.",
    "The first and second rules are that you're not supposed to talk about it."
  ], summary: "An unnamed, insomniac office worker forms an underground fight club with a charismatic soap salesman, which spirals into an anti-consumerist terrorist organization. He eventually discovers that the salesman is actually a hallucinated alter ego of his own fractured psyche." },

  { title: "Whiplash", reviews: [
    "An intense drama about obsession, ambition, and the brutal cost of greatness.",
    "A young drummer enrolls at an elite music conservatory hoping to become one of the greats.",
    "His conductor uses fear, humiliation, and thrown chairs as teaching tools.",
    "A bloody hand and a metronome ticking in his head define his relentless practice sessions.",
    "A car crash on the way to a competition doesn't stop him from crawling to his drum kit.",
    "A father-son style confrontation between the two ends in a triumphant solo performance."
  ], summary: "A driven young jazz drummer at an elite music school is pushed to his physical and psychological limits by an abusive, perfectionist conductor determined to find the next musical genius, culminating in a fierce, career-defining drum solo." },

  { title: "Everything Everywhere All at Once", reviews: [
    "A genre-blending sci-fi comedy about a woman overwhelmed by everything at once, literally.",
    "A laundromat owner facing an IRS audit discovers she can access the lives of her alternate selves.",
    "Her multiverse-jumping journey is triggered by an elevator ride with a very different version of her husband.",
    "Fights break out using absurd objects, including some memorably unconventional weapons.",
    "Two rocks sit quietly on a cliff for one of its most unexpectedly emotional scenes.",
    "A universe where everyone has hot dogs for fingers is just one of many bizarre realities she visits."
  ], summary: "An overwhelmed laundromat owner, in the middle of a tax audit, discovers she can jump between parallel versions of her life across the multiverse. She must use skills from her alternate selves to save reality from a powerful, nihilistic being while repairing her relationship with her daughter." },

  { title: "Oppenheimer", reviews: [
    "A tense biographical drama about a brilliant, morally conflicted scientist.",
    "A physicist is recruited to lead a secret government project in the New Mexico desert.",
    "His team races against time to build a weapon before a rival nation can.",
    "A silent countdown to a desert test culminates in an overwhelming display of light and sound.",
    "Years later, he faces a closed-door security hearing that threatens to unravel his legacy.",
    "He's remembered as the man who helped bring the atomic bomb into existence and spent the rest of his life wrestling with the consequences."
  ], summary: "Physicist J. Robert Oppenheimer leads the Manhattan Project's team of scientists in the New Mexico desert to develop the first atomic bomb during World War II. Years later, he faces a politically motivated security hearing that threatens to destroy his reputation over his guilt and later opposition to nuclear proliferation." },

  { title: "Knives Out", reviews: [
    "A stylish modern whodunit that plays with the classic murder-mystery formula.",
    "A wealthy mystery novelist is found dead the night after his birthday party.",
    "A mysterious detective with an unusual accent is hired anonymously to investigate.",
    "The victim's dysfunctional family members all seem to have their own motives to lie.",
    "His compassionate nurse has a strange physical reaction whenever she tells a lie.",
    "The detective's folksy manner masks a razor-sharp deductive mind as he unravels the family's web of secrets."
  ], summary: "When a wealthy crime novelist is found dead after his birthday party, an eccentric private detective is brought in to investigate his greedy, secretive family, uncovering a web of lies centered on the novelist's loyal caregiver." },

  { title: "Mad Max: Fury Road", reviews: [
    "A relentless, nearly wordless action epic set in a scorched post-apocalyptic wasteland.",
    "A wandering survivor is captured and used as a human blood bag by a cult-like warlord's army.",
    "A fierce rig driver breaks away from the warlord's convoy with his most prized possessions hidden aboard.",
    "The prized possessions turn out to be the warlord's captive brides, fleeing for freedom.",
    "Its two-hour runtime is essentially one continuous, thunderous vehicle chase across the desert.",
    "A war rig, a wandering drifter, and a one-armed rebel commander team up to outrun an army of chrome-obsessed warriors."
  ], summary: "In a desolate wasteland ruled by a tyrannical warlord, a rebel commander smuggles his five captive wives to freedom in a heavily armored war rig, forming an uneasy alliance with a haunted drifter as they outrun the warlord's relentless army across the desert." },

  { title: "A Quiet Place", reviews: [
    "A tense horror film built almost entirely around the absence of sound.",
    "A family navigates daily life in near-total silence after a global catastrophe.",
    "Blind creatures with hypersensitive hearing hunt anything that makes a noise.",
    "A pregnant mother has to prepare for a delivery she cannot afford to scream through.",
    "Sand paths and sign language become essential survival tools for the family.",
    "A nail sticking out of a staircase step becomes a small but terrifying hazard."
  ], summary: "In a world overrun by blind creatures that hunt by sound, a family survives by communicating in sign language and moving in near-total silence. Their fragile routine is tested when the mother must give birth while keeping deadly noise to an absolute minimum." },

  { title: "Die Hard", reviews: [
    "An action classic that became the blueprint for an entire genre of 'one guy against many' thrillers.",
    "An off-duty New York cop visits his estranged wife's office holiday party in Los Angeles.",
    "The party is interrupted by a group of thieves posing as terrorists to seize a corporate vault.",
    "He spends most of the film barefoot, having kicked off his shoes to relax before chaos erupts.",
    "A cop with nothing but a radio and a gun makes contact with a sympathetic officer outside.",
    "“Yippee-ki-yay” became an unlikely catchphrase from a skyscraper hostage standoff."
  ], summary: "An off-duty New York cop visiting his estranged wife's Los Angeles office Christmas party becomes the only one able to stop a group of thieves who seize the skyscraper under the guise of a terrorist takeover, picking them off one by one." },

  { title: "The Silence of the Lambs", reviews: [
    "A chilling psychological thriller pairing a young investigator with a brilliant, dangerous mind.",
    "A trainee FBI agent is sent to interview an imprisoned, highly intelligent cannibal for insight.",
    "The imprisoned killer agrees to help profile another active serial murderer, but only for a price.",
    "A moth's cocoon found in a victim's throat becomes a critical clue in the case.",
    "A killer lowers a basket on a rope to communicate with the agent through prison glass.",
    "The killer escapes custody with a chilling line about having an old friend for dinner."
  ], summary: "A young FBI trainee seeks the help of imprisoned cannibalistic psychiatrist Hannibal Lecter to catch a different serial killer who skins his victims. Her disturbing exchanges with Lecter lead her closer to the truth, even as he manipulates his way toward his own escape." },

  { title: "E.T. the Extra-Terrestrial", reviews: [
    "A tender science-fiction fable about childhood friendship and loneliness.",
    "A lonely boy discovers a stranded alien hiding in his family's garden shed.",
    "He hides the creature in his bedroom closet, disguising it among his stuffed toys.",
    "A bike ride silhouetted against a full moon became one of cinema's most iconic images.",
    "The boy and the alien share a strange psychic connection that lets them feel each other's emotions.",
    "“Phone home” became the catchphrase of a homesick visitor from another planet."
  ], summary: "A lonely boy befriends a gentle alien accidentally stranded on Earth and helps hide it from government agents while trying to find a way for it to contact its family and return home, forming a deep emotional bond along the way." },

  { title: "Barbie", reviews: [
    "A candy-colored comedy that turns a beloved toy brand into a surprisingly sharp piece of satire.",
    "A perfect resident of a pastel utopia starts having unsettling thoughts about mortality.",
    "She travels to the real world seeking the human child who's been playing with her too roughly.",
    "Her male counterpart tags along and discovers an entire philosophy about horses and patriarchy.",
    "A boardroom of executives at a toy company chases her around their headquarters in a farcical sequence.",
    "Her journey ends with a very human decision to trade plastic perfection for gynecological appointments."
  ], summary: "When a doll living in an idyllic pastel utopia begins having thoughts of death and imperfection, she travels to the real world to find the human causing her malfunction. Her journey — alongside her devoted companion, who discovers patriarchy — leads her to choose a flawed, mortal human existence over her plastic paradise." },

  { title: "Coco", reviews: [
    "A vibrant animated film about family, memory, and the importance of being remembered.",
    "A young boy from a family that has banned music dreams of becoming a musician anyway.",
    "He's accidentally transported to a vibrant land inhabited by the spirits of the dead.",
    "He needs a living family member's blessing to return home before sunrise.",
    "A skeletal dog with an oddly shaped tongue becomes his loyal guide through the spirit world.",
    "A beloved lullaby turns out to be the key to reuniting a family that lost its musical history generations ago."
  ], summary: "A young boy who dreams of becoming a musician, despite his family's generations-old ban on music, is accidentally transported to the Land of the Dead. There he uncovers his family's forgotten musical history and must earn a blessing to return home before sunrise." }
];

const MAX_GUESSES = 6;
let current = null;
let guesses = [];
let gameOver = false;
let won = false;
let mode = "daily";

function normalize(s) {
  return s.toLowerCase()
    .replace(/[^a-z0-9]/g, ' ')
    .replace(/^\s*(the|a|an)\s+/, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function dailyIndex() {
  const d = new Date();
  const seed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
  let h = 0;
  const s = String(seed);
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) >>> 0;
  return h % MOVIES.length;
}

function populateDatalist() {
  const list = document.getElementById('movieList');
  list.innerHTML = '';
  MOVIES.slice().sort((a,b) => a.title.localeCompare(b.title)).forEach(m => {
    const opt = document.createElement('option');
    opt.value = m.title;
    list.appendChild(opt);
  });
}

function startGame(newMode) {
  mode = newMode;
  gameOver = false;
  won = false;
  guesses = [];
  if (mode === "daily") {
    current = MOVIES[dailyIndex()];
  } else {
    let idx;
    do { idx = Math.floor(Math.random() * MOVIES.length); } while (MOVIES[idx] === current && MOVIES.length > 1);
    current = MOVIES[idx];
  }
  document.getElementById('guessInput').disabled = false;
  document.getElementById('submitBtn').disabled = false;
  document.getElementById('guessInput').value = '';
  document.getElementById('summarySlot').innerHTML = '';
  document.getElementById('shareSlot').innerHTML = '';
  document.getElementById('statusLine').textContent = '';
  document.getElementById('statusLine').className = 'status';
  render();
  document.getElementById('guessInput').focus();
}

function render() {
  const log = document.getElementById('reviewLog');
  log.innerHTML = '';
  const revealCount = Math.min(guesses.length + 1, MAX_GUESSES);
  for (let i = 0; i < revealCount; i++) {
    const row = document.createElement('div');
    row.className = 'review-row';
    row.innerHTML = `<span class="num">Review ${i + 1}</span><p>${current.reviews[i]}</p>`;
    log.appendChild(row);
  }

  const grid = document.getElementById('guessGrid');
  grid.innerHTML = '';
  for (let i = 0; i < MAX_GUESSES; i++) {
    const slot = document.createElement('div');
    if (i < guesses.length) {
      const g = guesses[i];
      slot.className = 'guess-slot ' + (g.correct ? 'correct' : 'wrong');
      slot.innerHTML = `<span class="idx">${i + 1}</span><span>${g.text}</span>`;
    } else {
      slot.className = 'guess-slot empty';
      slot.innerHTML = `<span class="idx">${i + 1}</span><span>—</span>`;
    }
    grid.appendChild(slot);
  }
}

function buildShareText() {
  const label = mode === 'daily' ? `Reviewdle ${new Date().toLocaleDateString()}` : 'Reviewdle (practice)';
  const line = guesses.map(g => g.correct ? '🟩' : '⬛').join('');
  const scoreText = won ? `${guesses.length}/6` : 'X/6';
  return `🎬 ${label} — ${scoreText}\n${line}`;
}

function endGame() {
  gameOver = true;
  document.getElementById('guessInput').disabled = true;
  document.getElementById('submitBtn').disabled = true;
  const statusLine = document.getElementById('statusLine');
  if (won) {
    statusLine.textContent = `Correct! It was "${current.title}."`;
    statusLine.className = 'status win';
  } else {
    statusLine.textContent = `Out of guesses. It was "${current.title}."`;
    statusLine.className = 'status lose';
    document.getElementById('summarySlot').innerHTML =
      `<div class="summary-box"><span class="label">PLOT SUMMARY</span>${current.summary}</div>`;
  }
  const shareText = buildShareText();
  document.getElementById('shareSlot').innerHTML =
    `<div class="share-box">${shareText}</div><div style="text-align:center"><button id="copyBtn">Copy Result</button></div>`;
  document.getElementById('copyBtn').addEventListener('click', () => {
    navigator.clipboard.writeText(shareText).then(() => {
      document.getElementById('copyBtn').textContent = 'Copied!';
      setTimeout(() => { document.getElementById('copyBtn').textContent = 'Copy Result'; }, 1500);
    });
  });
}

document.getElementById('guessForm').addEventListener('submit', (e) => {
  e.preventDefault();
  if (gameOver) return;
  const input = document.getElementById('guessInput');
  const val = input.value.trim();
  if (!val) return;
  const correct = normalize(val) === normalize(current.title);
  guesses.push({ text: val, correct });
  input.value = '';
  if (correct) {
    won = true;
    render();
    endGame();
  } else if (guesses.length >= MAX_GUESSES) {
    won = false;
    render();
    endGame();
  } else {
    render();
  }
});

document.getElementById('dailyBtn').addEventListener('click', () => startGame('daily'));
document.getElementById('randomBtn').addEventListener('click', () => startGame('random'));
document.getElementById('giveUpBtn').addEventListener('click', () => {
  if (gameOver) return;
  while (guesses.length < MAX_GUESSES) guesses.push({ text: '(skipped)', correct: false });
  won = false;
  render();
  endGame();
});
document.getElementById('howToLink').addEventListener('click', () => {
  document.getElementById('howTo').classList.toggle('show');
});

populateDatalist();
startGame('daily');

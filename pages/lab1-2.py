from env import HUGGING_FACE_TOKEN

from transformers import pipeline

# Hugging Face opensource usage

# Default model usage
generation = pipeline('text-generation', token=HUGGING_FACE_TOKEN)
print('Default model usage: ', generation('write a book about genAI'))

# Using a specific model
generation = pipeline(
  'text-generation', 
  model="openai-community/gpt2-large", 
  token=HUGGING_FACE_TOKEN
  )
print('Specific model usage: ', generation('write a book about genAI'))

# Using a parameterized model
temperature_value = 0.8
top_p_value = 0.9
max_length_value = 100

generation = pipeline('text-generation', token=HUGGING_FACE_TOKEN)
prompt = "write a book about AI"
output = generation(
prompt,
max_length=max_length_value,
temperature=temperature_value,
top_p=top_p_value
)
print('Parametrized model usage: ', output[0]['generated_text'])

# Using summarization model
temperature_value = 0.8
top_p_value = 0.9
max_length_value = 100

generation = pipeline('summarization', token=HUGGING_FACE_TOKEN)
prompt = """
Once upon a time, in a lush, green forest filled with towering trees and sparkling streams, there lived a little bear named Benji. Benji wasn’t like the other bears. While most of his bear family liked to spend their days hunting for honey and fishing by the river, Benji had a different passion—he loved exploring.

Every day, as the sun began to rise, Benji would leave his cozy cave, his little heart racing with excitement for the day ahead. He would wander through the woods, his small paws patting the soft earth beneath him, and his big brown eyes taking in everything—the way the leaves danced in the breeze, the sound of the birds chirping, and the scent of wildflowers that filled the air.

One bright morning, while walking near a sparkling brook, Benji spotted something shiny and unusual in the distance. Curious, he padded closer and found a beautiful stone, smooth and glimmering in the sunlight. It was unlike anything he had ever seen! Benji carefully picked it up with his tiny paws and marveled at its beauty.

But as he was admiring the stone, a gentle voice called out from the bushes. "What have you got there, little bear?"

Startled, Benji turned around to see an old, wise owl perched on a nearby tree branch. The owl’s feathers were soft and grey, and her eyes were large and kind.

"I found this shiny stone," Benji said, holding it out for the owl to see. "Is it special?"

The owl hooted softly, nodding. "Ah, that stone is special indeed. It’s a wishing stone, Benji. You can make one wish, but only if it comes from your heart."

Benji’s eyes widened. "A wishing stone? What should I wish for?"

The owl looked at him thoughtfully. "A wish should not be made for things that can be seen or touched, young one. True wishes come from the heart. Think carefully."

Benji held the stone in his paws and thought about the world around him. His mind raced through all the things he could wish for—honey, bigger paws, a new adventure—but then something else came to his mind. A wish that felt just right.

With a deep breath, Benji closed his eyes, held the stone close to his heart, and made his wish: "I wish to always find happiness in the little things, no matter where I go."

The stone shimmered and glowed for a moment, then became still. The owl smiled gently. "That, dear Benji, is a beautiful wish."

From that day forward, Benji found joy in every step of his adventure. Whether it was watching the sun paint the sky with colors at dawn, listening to the rustle of the leaves as the wind passed through, or sharing a quiet moment with a butterfly, Benji learned that true happiness wasn’t something you could hold in your paws—it was in the simple, beautiful things all around you.

And so, Benji continued his journey through the forest, his heart light and full of wonder, always cherishing the little moments that made life so special.

The End.
"""
output = generation(
prompt,
max_length=max_length_value,
temperature=temperature_value,
top_p=top_p_value
)
print('Summarization model usage: ', output[0]['summary_text'])

# Using sentiment analysis model
sentiment_pipeline = pipeline(
  "sentiment-analysis", 
  model="tabularisai/multilingual-sentiment-analysis", 
  token=HUGGING_FACE_TOKEN
  )
data = [
  "I love spending time with my family and friends.",
  "The weather is terrible today, and everything went wrong.",
  "The concert last night was amazing! The performers were outstanding.",
  "I'm feeling indifferent about the upcoming changes at work.",
  "The customer service representative was rude and unhelpful.",
  "This new technology is groundbreaking and will revolutionize the industry.",
  "Finding a solution to the problem was more difficult than I anticipated.",
  "Attending the conference was a valuable experience for my professional growth.",
  "I feel content and at peace when I'm surrounded by nature.",
  "The traffic today was unbearable, and I got stuck for hours.",
  "Discovering new cultures through travel is always exciting."
]
sentiment_result = sentiment_pipeline(data)
print('Sentiment analysis model usage: ', sentiment_result)

expected_result = [
  "Positive",
  "Negative",
  "Positive",
  "Neutral",
  "Negative",
  "Positive",
  "Negative",
  "Positive",
  "Positive",
  "Negative",
  "Positive"
]

wrong_results = [i for i, (result, expected) in enumerate(zip(sentiment_result, expected_result)) if result['label'].lower() != expected.lower()]
wrong_results
print("Wrong results:")
for i in wrong_results:
  print(f"{data[i]}; Expected result: {expected_result[i]}; Actual result: {sentiment_result[i]['label']}")

# Using translation model
translation = pipeline("translation_en_to_fr", token=HUGGING_FACE_TOKEN)
temperature_value = 0.8
top_p_value = 0.9
max_length_value = 100
data = [
  "Challenges are opportunities in disguise.",
  "Innovation is the cornerstone of progress in the 21st century."
]

print("Translation model usage: ", translation(data))
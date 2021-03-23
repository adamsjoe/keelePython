# After following the above examples you should be capable of writing code that answers the following questions:

# Who is tall, fast and bilingual ?
# Who is bilingual, but not tall ?

tall = {"Tom", "Bob", "Harry", "Susan", "Phillipa", "Mike"}
fast = {"Tom", "Harry", "Phillipa", "Keith", "Brian"}
bilingual = {"Harry", "Susan", "Brian", "Robert"}

tall_fast_biligual = bilingual.intersection(fast, tall)
print(tall_fast_biligual, " is tall, fast and bilingual")

bilingual_notTall = tall.difference(bilingual)
print(bilingual_notTall)
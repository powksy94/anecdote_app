import '../lib/data/verified_animals.dart';

void main() {
  final now = DateTime.now();
  final dayOfYear = now.difference(DateTime(now.year, 1, 1)).inDays;
  final animalKeys = verifiedAnimals.keys.toList();
  final index = dayOfYear % animalKeys.length;
  final selectedAnimal = animalKeys[index];

  print('Date: $now');
  print('Day of year: $dayOfYear');
  print('Total animals: ${animalKeys.length}');
  print('Index: $index');
  print('Selected animal: $selectedAnimal');
  print('API name: ${verifiedAnimals[selectedAnimal]}');
  print('URL: https://api.api-ninjas.com/v1/animals?name=${Uri.encodeComponent(selectedAnimal)}');
}

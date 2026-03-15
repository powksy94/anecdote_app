import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;

const apiKey = 'hsXlM6fqeIOFEVrkhjOYM7iISwCFnkcuHAEP3556';

const List<String> animalsToTest = [
  'lion', 'elephant', 'tiger', 'wolf', 'eagle', 'dolphin', 'bear', 'fox',
  'giraffe', 'zebra', 'kangaroo', 'penguin', 'panda', 'koala', 'gorilla',
  'cheetah', 'leopard', 'jaguar', 'rhino', 'hippo', 'crocodile', 'shark',
  'whale', 'octopus', 'owl', 'parrot', 'flamingo', 'peacock', 'swan', 'horse',
  'camel', 'llama', 'deer', 'moose', 'bison', 'buffalo', 'chimpanzee',
  'orangutan', 'lemur', 'sloth', 'armadillo', 'anteater', 'hedgehog',
  'raccoon', 'badger', 'otter', 'beaver', 'squirrel', 'rabbit', 'hamster',
  'snake', 'lizard', 'turtle', 'frog', 'salamander', 'jellyfish', 'starfish',
  'crab', 'lobster', 'shrimp', 'seal', 'walrus', 'polar bear', 'arctic fox',
  'reindeer', 'wolverine', 'lynx', 'cougar', 'hyena', 'jackal', 'meerkat',
  'mongoose', 'warthog', 'antelope', 'gazelle', 'ibex', 'yak', 'tapir',
  'okapi', 'capybara', 'porcupine', 'bat', 'hummingbird', 'toucan', 'pelican',
  'albatross', 'condor', 'falcon', 'hawk', 'vulture', 'ostrich', 'emu',
  'kiwi', 'cassowary', 'platypus', 'echidna', 'tasmanian devil', 'wombat',
  'dingo', 'komodo dragon', 'iguana', 'chameleon', 'gecko', 'python', 'cobra',
  'manta ray', 'swordfish', 'marlin', 'tuna', 'salmon', 'piranha',
  'electric eel', 'seahorse', 'clownfish', 'angelfish', 'barracuda',
  'manatee', 'narwhal', 'beluga', 'orca', 'humpback whale', 'blue whale',
];

Future<void> main() async {
  final Map<String, String> verifiedAnimals = {};
  final List<String> failedAnimals = [];

  print('Testing ${animalsToTest.length} animals...\n');

  for (int i = 0; i < animalsToTest.length; i++) {
    final animal = animalsToTest[i];
    stdout.write('Testing "${animal}" (${i + 1}/${animalsToTest.length})... ');

    try {
      final response = await http.get(
        Uri.parse('https://api.api-ninjas.com/v1/animals?name=${Uri.encodeComponent(animal)}'),
        headers: {'X-Api-Key': apiKey},
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        final decoded = jsonDecode(response.body);
        if (decoded is List && decoded.isNotEmpty) {
          final apiName = decoded[0]['name'] as String;
          verifiedAnimals[animal] = apiName;
          print('OK -> "$apiName"');
        } else {
          failedAnimals.add(animal);
          print('EMPTY');
        }
      } else {
        failedAnimals.add(animal);
        print('ERROR ${response.statusCode}');
      }
    } catch (e) {
      failedAnimals.add(animal);
      print('FAILED: $e');
    }

    await Future.delayed(const Duration(milliseconds: 200));
  }

  print('\n${'=' * 50}');
  print('RESULTS:');
  print('  Verified: ${verifiedAnimals.length}');
  print('  Failed: ${failedAnimals.length}');
  print('${'=' * 50}\n');

  if (failedAnimals.isNotEmpty) {
    print('Failed animals:');
    for (final animal in failedAnimals) {
      print('  - $animal');
    }
    print('');
  }

  final buffer = StringBuffer();
  buffer.writeln('const Map<String, String> verifiedAnimals = {');
  verifiedAnimals.forEach((key, value) {
    buffer.writeln("  '$key': '$value',");
  });
  buffer.writeln('};');

  final outputFile = File('lib/data/verified_animals.dart');
  await outputFile.writeAsString(buffer.toString());
  print('Verified animals saved to: lib/data/verified_animals.dart');
}

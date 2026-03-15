import 'dart:convert';
import 'package:http/http.dart' as http;

const apiKey = 'hsXlM6fqeIOFEVrkhjOYM7iISwCFnkcuHAEP3556';

Future<void> main() async {
  final now = DateTime.now();
  final url = 'https://api.api-ninjas.com/v1/historicalevents?month=${now.month}&day=${now.day}';

  print('Date actuelle: ${now.day}/${now.month}/${now.year}');
  print('URL: $url');
  print('');

  final response = await http.get(
    Uri.parse(url),
    headers: {'X-Api-Key': apiKey},
  );

  print('Status: ${response.statusCode}');

  final decoded = jsonDecode(response.body);
  if (decoded is List) {
    print('Nombre de resultats: ${decoded.length}');
    print('');
    for (int i = 0; i < decoded.length && i < 5; i++) {
      final event = decoded[i];
      print('--- Event ${i + 1} ---');
      print('Year: ${event['year']}');
      print('Month: ${event['month']}');
      print('Day: ${event['day']}');
      print('Event: ${event['event']}');
      print('');
    }
  }
}

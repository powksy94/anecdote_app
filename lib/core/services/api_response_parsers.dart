import 'dart:convert';
import 'package:http/http.dart' as http;
import '../models/content_type.dart';
import '../models/content_data.dart';
import '../../features/science/data/verified_animals.dart';

int dayOfYear() {
  final now = DateTime.now();
  final todayUtc = DateTime.utc(now.year, now.month, now.day);
  return todayUtc.difference(DateTime.utc(now.year, 1, 1)).inDays;
}

ContentData parseApiResponse(ContentType type, dynamic decoded) {
  switch (type) {
    case ContentType.anecdote:       return parseAnecdote(decoded);
    case ContentType.chuckNorris:    return parseChuckNorris(decoded);
    case ContentType.celebrityQuote: return parseCelebrityQuote(decoded);
    case ContentType.history:        return parseHistory(decoded);
    case ContentType.animals:        return parseAnimals(decoded);
    default:                         return ContentData(preview: 'Content not available');
  }
}

ContentData parseAnecdote(dynamic decoded) {
  if (decoded is List && decoded.isNotEmpty) {
    return ContentData(preview: decoded[0]['fact'] ?? 'No content');
  }
  return ContentData(preview: 'Content not available');
}

ContentData parseChuckNorris(dynamic decoded) {
  if (decoded is Map) return ContentData(preview: decoded['joke'] ?? 'No joke');
  return ContentData(preview: 'Content not available');
}

ContentData parseCelebrityQuote(dynamic decoded) {
  if (decoded is List && decoded.isNotEmpty) {
    return ContentData(
      preview: '"${decoded[0]['quote'] ?? ''}"',
      details: '— ${decoded[0]['author'] ?? 'Anonymous'}',
      hasDetails: true,
    );
  }
  return ContentData(preview: 'Content not available');
}

ContentData parseHistory(dynamic decoded) {
  if (decoded is! List || decoded.isEmpty) return ContentData(preview: 'Content not available');
  final event   = decoded[0];
  final rawYear = event['year'] as String? ?? '';
  final yearInt = int.tryParse(rawYear);
  final String displayYear;
  if (yearInt == null) {
    displayYear = '';
  } else if (yearInt < 0) {
    displayYear = '${yearInt.abs()} BC';
  } else {
    displayYear = yearInt.toString();
  }
  final eventText = (event['event'] as String? ?? '').replaceAll(RegExp(r'\[[^\]]*\]'), '').trim();
  final now    = DateTime.now();
  final months = ['','January','February','March','April','May','June','July',
                  'August','September','October','November','December'];
  final day    = now.day;
  final suffix = day == 1 ? 'st' : day == 2 ? 'nd' : day == 3 ? 'rd' : 'th';
  final datePart = displayYear.isEmpty
      ? '$day$suffix ${months[now.month]}'
      : '$day$suffix ${months[now.month]} $displayYear';
  return ContentData(preview: '$datePart\n\n$eventText');
}

ContentData parseAnimals(dynamic decoded) {
  if (decoded is! List || decoded.isEmpty) return ContentData(preview: 'Content not available');
  final animal          = decoded[0];
  final name            = animal['name'] ?? 'Unknown';
  final taxonomy        = animal['taxonomy']        as Map<String, dynamic>? ?? {};
  final characteristics = animal['characteristics'] as Map<String, dynamic>? ?? {};
  final locations       = animal['locations']       as List? ?? [];
  final searchKey       = verifiedAnimals.keys.toList()[dayOfYear() % verifiedAnimals.length];
  final emoji           = animalEmojis[searchKey] ?? '🐾';
  final buf = StringBuffer();
  if (taxonomy.isNotEmpty) {
    buf.writeln('📚 TAXONOMY');
    for (final k in ['kingdom','phylum','class','order','family','genus','scientific_name']) {
      if (taxonomy[k] != null) {
        buf.writeln('  ${k == 'scientific_name' ? 'Scientific name' : k[0].toUpperCase() + k.substring(1)}: ${taxonomy[k]}');
      }
    }
    buf.writeln('');
  }
  if (characteristics.isNotEmpty) {
    buf.writeln('📊 CHARACTERISTICS');
    for (final k in ['lifespan','weight','height','length','top_speed','diet','habitat','prey','predators']) {
      if (characteristics[k] != null) {
        buf.writeln('  ${k[0].toUpperCase() + k.substring(1).replaceAll('_', ' ')}: ${characteristics[k]}');
      }
    }
    buf.writeln('');
  }
  if (locations.isNotEmpty) {
    buf.writeln('📍 LOCATION');
    buf.writeln('  ${locations.join(', ')}');
  }
  return ContentData(preview: '$emoji $name', details: buf.toString().trim(), hasDetails: true);
}

Future<String?> fetchWikiImage(String name) async {
  try {
    final url = 'https://en.wikipedia.org/api/rest_v1/page/summary/${Uri.encodeComponent(name)}';
    final r = await http.get(Uri.parse(url)).timeout(const Duration(seconds: 5));
    if (r.statusCode == 200) {
      return (jsonDecode(r.body) as Map<String, dynamic>)['thumbnail']?['source'] as String?;
    }
  } catch (_) {}
  return null;
}

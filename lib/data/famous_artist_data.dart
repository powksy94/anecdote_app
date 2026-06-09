import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

// n=name, na=nationality, bo=born, di=died, mo=movement, fa=famous_for, im=imageUrl, wl=warningLevel, wi=warningText

class FamousArtistData {
  final String name, nationality, born, died, movement, famousFor;
  final String? imageUrl;
  final String? warningLevel;
  final String? warningText;

  const FamousArtistData({
    required this.name, required this.nationality, required this.born,
    required this.died, required this.movement, required this.famousFor,
    this.imageUrl, this.warningLevel, this.warningText,
  });

  factory FamousArtistData.fromJson(Map<String, dynamic> j) => FamousArtistData(
    name:         j['n']  ?? '',
    nationality:  j['na'] ?? '',
    born:         j['bo'] ?? '',
    died:         j['di'] ?? '',
    movement:     j['mo'] ?? '',
    famousFor:    j['fa'] ?? '',
    imageUrl:     j['im'] as String?,
    warningLevel: j['wl'] as String?,
    warningText:  j['wi'] as String?,
  );

  String? get noImageMessage {
    if (imageUrl != null) return null;
    return '🎨 No image available for this artist';
  }
}

Future<List<FamousArtistData>> loadFamousArtists() async {
  final raw = await rootBundle.loadString('assets/art/famous_artists.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => FamousArtistData.fromJson(e as Map<String, dynamic>)).toList();
}

List<FamousArtistData>? _shuffledCache;

FamousArtistData dailyFamousArtist(List<FamousArtistData> artists) {
  if (_shuffledCache == null) {
    final list = List<FamousArtistData>.from(artists);
    final rng = math.Random(20260203);
    for (int i = list.length - 1; i > 0; i--) {
      final j = rng.nextInt(i + 1);
      final tmp = list[i]; list[i] = list[j]; list[j] = tmp;
    }
    _shuffledCache = list;
  }
  final now = DateTime.now();
  final today = DateTime.utc(now.year, now.month, now.day);
  final origin = DateTime.utc(2026, 1, 1);
  final index = today.difference(origin).inDays.abs();
  return _shuffledCache![index % _shuffledCache!.length];
}

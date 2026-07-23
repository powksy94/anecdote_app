import 'dart:convert';
import 'dart:math' as math;
import 'package:flutter/services.dart';

class AlbumData {
  final String title, artist, sales, famousFor;
  final String? imageUrl;
  final int year;

  const AlbumData({
    required this.title, required this.artist, required this.sales,
    required this.famousFor, required this.year, this.imageUrl,
  });

  String? get noImageMessage => imageUrl != null ? null : '💿 No cover art available for this album';

  factory AlbumData.fromJson(Map<String, dynamic> j) => AlbumData(
    title:      j['n']  ?? '',
    artist:     j['ar'] ?? '',
    sales:      j['sa'] ?? '',
    famousFor:  j['fa'] ?? '',
    year:       (j['yr'] as num?)?.toInt() ?? 0,
    imageUrl:   j['im'] as String?,
  );
}

Future<List<AlbumData>> loadAlbums() async {
  final raw = await rootBundle.loadString('assets/music/albums.json');
  final list = jsonDecode(raw) as List;
  return list.map((e) => AlbumData.fromJson(e as Map<String, dynamic>)).toList();
}

List<AlbumData>? _shuffledCache;

AlbumData dailyAlbum(List<AlbumData> albums) {
  if (_shuffledCache == null) {
    final list = List<AlbumData>.from(albums);
    final rng = math.Random(20260202);
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

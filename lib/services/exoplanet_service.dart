import 'dart:convert';
import 'package:flutter/services.dart';
import '../data/exoplanet.dart';
import '../models/content_data.dart';

class ExoplanetService {
  static List<Exoplanet>? _cache;

  Future<List<Exoplanet>> _loadPlanets() async {
    if (_cache != null) return _cache!;
    final raw = await rootBundle.loadString('assets/exoplanets.json');
    final list = jsonDecode(raw) as List<dynamic>;
    _cache = list
        .map((e) => Exoplanet.fromJson(e as Map<String, dynamic>))
        .toList();
    return _cache!;
  }

  Future<ContentData> getDailyContent() async {
    final planets = await _loadPlanets();
    final planet = dailyExoplanet(planets);
    return _buildContentData(planet);
  }

  ContentData _buildContentData(Exoplanet p) {
    final preview = '🪐 ${p.name}\nOrbits ${p.host} · Discovered ${p.year}';

    final buf = StringBuffer();

    buf.writeln('🔭 Discovery');
    buf.writeln('🛸 Method: ${p.method}');
    if (p.facility.isNotEmpty) buf.writeln('🏔️ Observatory: ${p.facility}');

    buf.writeln('📏 Size & Mass');
    if (p.rade != null) buf.writeln('🌍 Radius: ${p.rade}× Earth');
    if (p.radj != null) buf.writeln('🪐 Radius: ${p.radj}× Jupiter');
    if (p.masse != null) buf.writeln('⚖️ Mass: ${p.masse}× Earth');

    if (p.orbper != null) buf.writeln('⏱️ Orbital period: ${p.orbper} days');
    if (p.eqt != null) {
      final celsius = (p.eqt! - 273.15).round();
      buf.writeln('🌡️ Temperature: ${p.eqt!.round()} K ($celsius °C)');
    }

    buf.writeln('⭐ Host Star: ${p.host}');
    if (p.spectype.isNotEmpty) buf.writeln('✨ Spectral type: ${p.spectype}');
    if (p.steff != null) buf.writeln('🔥 Temperature: ${p.steff!.round()} K');

    buf.writeln('📡 Location in the sky');
    if (p.dist != null) {
      final ly = (p.dist! * 3.26156).toStringAsFixed(1);
      buf.writeln('📐 Distance: ${p.dist} pc ($ly light-years)');
    }
    if (p.rastr.isNotEmpty) buf.writeln('↗️ Right ascension: ${p.rastr}');
    if (p.decstr.isNotEmpty) buf.writeln('↕️ Declination: ${p.decstr}');

    return ContentData(
      preview: preview,
      details: buf.toString().trim(),
      hasDetails: true,
    );
  }
}

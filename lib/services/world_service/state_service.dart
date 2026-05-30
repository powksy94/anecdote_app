import '../../data/state_data.dart';
import '../../models/content_data.dart';

class StateService {
  static List<StateData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadStates();
    final s = dailyState(_cache!);

    final buf = StringBuffer();
    buf.writeln('🏛️ Capital: ${s.capital}');
    buf.writeln('🌟 Nickname: ${s.nickname}');
    buf.writeln('📍 Region: ${s.region}');
    buf.writeln('👥 Population: ${_formatPop(s.population)}');
    buf.writeln('📐 Area: ${_formatArea(s.area)} km²');
    buf.writeln('📅 Statehood: ${s.statehoodYear}');
    buf.writeln('💡 ${s.famousFor}');

    return ContentData(
      preview: '🗺️ ${s.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: s.imageUrl,
      noImageMessage: s.noImageMessage,
    );
  }

  String _formatPop(int pop) {
    if (pop >= 1000000000) return '${(pop / 1e9).toStringAsFixed(1)}B';
    if (pop >= 1000000)    return '${(pop / 1e6).toStringAsFixed(1)}M';
    if (pop >= 1000)       return '${(pop / 1000).toStringAsFixed(0)}K';
    return '$pop';
  }

  String _formatArea(int area) =>
      area.toString().replaceAllMapped(
        RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (m) => '${m[1]},');
}

import '../../data/department_data.dart';
import '../../models/content_data.dart';

class DepartmentService {
  static List<DepartmentData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadDepartments();
    final d = dailyDepartment(_cache!);

    final buf = StringBuffer();
    if (d.prefecture.isNotEmpty)  { buf.writeln('🏛️ Prefecture: ${d.prefecture}'); }
    if (d.region.isNotEmpty)      { buf.writeln('🌐 Region: ${d.region}'); }
    if (d.population != null) {
      final pop = d.population!;
      final String fmt;
      if (pop >= 1000000)       { fmt = '${(pop / 1e6).toStringAsFixed(1)}M'; }
      else if (pop >= 1000)     { fmt = '${(pop / 1000).toStringAsFixed(0)}K'; }
      else                      { fmt = '$pop';}
      buf.writeln('👥 Population: $fmt');
    }
    if (d.area != null) {
      buf.writeln('📐 Area: ${d.area!.toString().replaceAllMapped(RegExp(r'(\d{1,3})(?=(\d{3})+(?!\d))'), (m) => '${m[1]},')} km²');
    }

    return ContentData(
      preview: '🇫🇷 ${d.code} - ${d.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: d.imageUrl,
      noImageMessage: d.noImageMessage,
    );
  }
}
import '../data/space_mission_data.dart';
import '../../../core/models/content_data.dart';

class SpaceMissionService {
  static List<SpaceMissionData>? _cache;

  Future<ContentData> getDailyContent() async {
    _cache ??= await loadSpaceMissions();
    final m = dailySpaceMission(_cache!);

    final statusIcon = _statusIcon(m.status);
    final buf = StringBuffer();
    buf.writeln('🏢 Agency: ${m.agency}');
    buf.writeln('🎯 Destination: ${m.destination}');
    buf.writeln('📅 Launch: ${m.launchYear}');
    buf.writeln('⏱️ Duration: ${m.duration}');
    buf.writeln('$statusIcon Status: ${m.status}');
    buf.writeln('💡 ${m.famousFor}');

    return ContentData(
      preview: '🚀 ${m.name}',
      details: buf.toString().trim(),
      hasDetails: true,
      imageUrl: m.imageUrl,
    );
  }

  String _statusIcon(String status) {
    switch (status) {
      case 'Success': return '✅';
      case 'Failure': return '❌';
      case 'Ongoing': return '🔄';
      case 'Partial': return '⚠️';
      default:        return '❓';
    }
  }
}

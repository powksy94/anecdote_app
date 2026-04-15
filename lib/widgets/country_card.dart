import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../generated/app_localizations.dart';
import '../models/content_data.dart';

class CountryCard extends StatelessWidget {
  final ContentData? contentData;
  final List<Color> gradient;
  final Color accentColor;
  final String timeUntilMidnight;

  const CountryCard({
    super.key,
    required this.contentData,
    required this.gradient,
    required this.accentColor,
    required this.timeUntilMidnight,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final preview = contentData?.preview ?? '';
    final emojiFlag = RegExp(r'[\u{1F1E0}-\u{1F1FF}]{2}', unicode: true)
            .firstMatch(preview)
            ?.group(0) ??
        '🌍';
    final countryName = preview
        .replaceAll(RegExp(r'[\u{1F1E0}-\u{1F1FF}]{2}\s*', unicode: true), '')
        .trim();
    final detailLines = (contentData?.details ?? '')
        .split('\n')
        .where((l) => l.trim().isNotEmpty)
        .toList();

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24),
      child: Column(
        children: [
          Container(
            width: double.infinity,
            constraints: const BoxConstraints(maxWidth: 400),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              borderRadius: BorderRadius.circular(24),
              boxShadow: [
                BoxShadow(
                  color: accentColor.withValues(alpha: 0.3),
                  blurRadius: 30,
                  spreadRadius: 5,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ClipRRect(
                  borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
                  child: contentData?.flagSvg != null
                      ? SvgPicture.string(
                          contentData!.flagSvg!,
                          width: double.infinity,
                          fit: BoxFit.fitWidth,
                        )
                      : Container(
                          height: 160,
                          decoration: BoxDecoration(gradient: LinearGradient(colors: gradient)),
                          child: Center(
                            child: Text(emojiFlag, style: const TextStyle(fontSize: 100)),
                          ),
                        ),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(24, 20, 24, 4),
                  child: Text(
                    countryName,
                    textAlign: TextAlign.center,
                    style: theme.textTheme.headlineSmall?.copyWith(fontWeight: FontWeight.bold),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 24),
                  child: Divider(color: accentColor.withValues(alpha: 0.3)),
                ),
                Padding(
                  padding: const EdgeInsets.fromLTRB(24, 8, 24, 20),
                  child: Column(
                    children: detailLines.map((line) {
                      final parts = line.split(':');
                      final label = parts[0].trim();
                      final value = parts.length > 1 ? parts.sublist(1).join(':').trim() : '';
                      return Padding(
                        padding: const EdgeInsets.symmetric(vertical: 6),
                        child: Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              label,
                              style: theme.textTheme.bodyMedium
                                  ?.copyWith(fontWeight: FontWeight.w600),
                            ),
                            if (value.isNotEmpty) ...[
                              const SizedBox(width: 4),
                              const Text(':'),
                              const SizedBox(width: 6),
                              Expanded(
                                child: Text(
                                  value,
                                  style: theme.textTheme.bodyMedium?.copyWith(
                                    color: theme.colorScheme.onSurface.withValues(alpha: 0.75),
                                  ),
                                ),
                              ),
                            ],
                          ],
                        ),
                      );
                    }).toList(),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.only(bottom: 20),
                  child: Center(
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.schedule_rounded, size: 16, color: accentColor),
                          const SizedBox(width: 8),
                          Text(
                            loc.newContentIn(timeUntilMidnight),
                            style: TextStyle(
                              fontSize: 13,
                              color: accentColor,
                              fontWeight: FontWeight.w500,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

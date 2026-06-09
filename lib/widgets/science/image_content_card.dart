import 'package:flutter/material.dart';
import '../../generated/app_localizations.dart';
import '../../models/content_data.dart';
import '../../models/content_type.dart';
import '../cinema/cinema_toggle_section.dart';
import '../cinema/cinema_timer_badge.dart';
import '../warning_badge.dart';
import 'image_header.dart';

class ImageContentCard extends StatefulWidget {
  final ContentData? contentData;
  final ContentType contentType;
  final List<Color> gradient;
  final Color accentColor;
  final String timeUntilMidnight;

  const ImageContentCard({
    super.key,
    required this.contentData,
    required this.contentType,
    required this.gradient,
    required this.accentColor,
    required this.timeUntilMidnight,
  });

  @override
  State<ImageContentCard> createState() => _ImageContentCardState();
}

class _ImageContentCardState extends State<ImageContentCard> {
  bool _showDetails = false;

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;

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
                  color: widget.accentColor.withValues(alpha: 0.3),
                  blurRadius: 30,
                  spreadRadius: 5,
                  offset: const Offset(0, 10),
                ),
              ],
            ),
            child: Column(
              children: [
                ImageHeader(
                  imageUrl: widget.contentData?.imageUrl,
                  gradient: widget.gradient,
                  fallbackIcon: widget.contentType.icon,
                  noImageMessage: widget.contentData?.noImageMessage,
                ),
                Padding(
                  padding: const EdgeInsets.all(24),
                  child: Column(
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          Flexible(
                            child: Text(
                              widget.contentData?.preview ?? '',
                              textAlign: TextAlign.center,
                              style: theme.textTheme.titleLarge?.copyWith(
                                fontWeight: FontWeight.bold,
                                height: 1.3,
                              ),
                            ),
                          ),
                          if (widget.contentData?.warningText != null) ...[
                            const SizedBox(width: 8),
                            WarningBadge(
                              text: widget.contentData!.warningText!,
                              level: widget.contentData!.warningLevel ?? 'orange',
                            ),
                          ],
                        ],
                      ),
                      if (widget.contentData?.hasDetails == true) ...[
                        const SizedBox(height: 16),
                        CinemaToggleSection(
                          label: _showDetails ? loc.hideDetails : loc.showDetails,
                          icon: Icons.visibility_rounded,
                          accentColor: widget.accentColor,
                          isExpanded: _showDetails,
                          onTap: () => setState(() => _showDetails = !_showDetails),
                          content: widget.contentData?.details ?? '',
                          contentStyle: theme.textTheme.bodyMedium?.copyWith(height: 1.6),
                        ),
                      ],
                      const SizedBox(height: 20),
                      CinemaTimerBadge(
                        timeUntilMidnight: widget.timeUntilMidnight,
                        accentColor: widget.accentColor,
                      ),
                    ],
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

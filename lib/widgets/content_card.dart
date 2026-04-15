import 'package:flutter/material.dart';
import '../generated/app_localizations.dart';
import '../models/content_data.dart';
import '../models/content_type.dart';

class ContentCard extends StatefulWidget {
  final ContentData? contentData;
  final ContentType contentType;
  final List<Color> gradient;
  final Color accentColor;
  final String timeUntilMidnight;

  const ContentCard({
    super.key,
    required this.contentData,
    required this.contentType,
    required this.gradient,
    required this.accentColor,
    required this.timeUntilMidnight,
  });

  @override
  State<ContentCard> createState() => _ContentCardState();
}

class _ContentCardState extends State<ContentCard> {
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
            padding: const EdgeInsets.all(24),
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
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: widget.gradient),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Icon(widget.contentType.icon, size: 40, color: Colors.white),
                ),
                const SizedBox(height: 24),
                Text(
                  widget.contentData?.preview ?? '',
                  textAlign: TextAlign.center,
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontSize: 20,
                    height: 1.5,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                if (widget.contentData?.hasDetails == true) ...[
                  const SizedBox(height: 20),
                  GestureDetector(
                    onTap: () => setState(() => _showDetails = !_showDetails),
                    child: Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 12),
                      decoration: BoxDecoration(
                        gradient: LinearGradient(
                          colors: [
                            widget.accentColor.withValues(alpha: 0.15),
                            widget.accentColor.withValues(alpha: 0.08),
                          ],
                        ),
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            _showDetails
                                ? Icons.visibility_off_rounded
                                : Icons.visibility_rounded,
                            size: 20,
                            color: widget.accentColor,
                          ),
                          const SizedBox(width: 8),
                          Text(
                            _showDetails ? loc.hideDetails : loc.showDetails,
                            style: TextStyle(
                              fontSize: 14,
                              color: widget.accentColor,
                              fontWeight: FontWeight.w600,
                            ),
                          ),
                          const SizedBox(width: 4),
                          AnimatedRotation(
                            turns: _showDetails ? 0.5 : 0,
                            duration: const Duration(milliseconds: 200),
                            child: Icon(
                              Icons.keyboard_arrow_down_rounded,
                              size: 20,
                              color: widget.accentColor,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  AnimatedCrossFade(
                    firstChild: const SizedBox.shrink(),
                    secondChild: Container(
                      width: double.infinity,
                      margin: const EdgeInsets.only(top: 16),
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                        borderRadius: BorderRadius.circular(16),
                        border: Border.all(
                          color: widget.accentColor.withValues(alpha: 0.2),
                          width: 1,
                        ),
                      ),
                      child: Text(
                        widget.contentData?.details ?? '',
                        style: theme.textTheme.bodyMedium?.copyWith(height: 1.6),
                      ),
                    ),
                    crossFadeState:
                        _showDetails ? CrossFadeState.showSecond : CrossFadeState.showFirst,
                    duration: const Duration(milliseconds: 300),
                  ),
                ],
                const SizedBox(height: 20),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                  decoration: BoxDecoration(
                    color: theme.colorScheme.surfaceContainerHighest.withValues(alpha: 0.5),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Icon(Icons.schedule_rounded, size: 16, color: widget.accentColor),
                      const SizedBox(width: 8),
                      Text(
                        loc.newContentIn(widget.timeUntilMidnight),
                        style: TextStyle(
                          fontSize: 13,
                          color: widget.accentColor,
                          fontWeight: FontWeight.w500,
                        ),
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

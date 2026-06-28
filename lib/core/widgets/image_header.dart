import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter_cache_manager/flutter_cache_manager.dart';
import 'package:flutter/material.dart';
import '../../generated/app_localizations.dart';

class ImageHeader extends StatefulWidget {
  final String? imageUrl;
  final List<Color> gradient;
  final IconData fallbackIcon;
  final String? noImageMessage;
  final String? noImageTitle;
  final String? noImageExplanation;
  final String? elementSymbol;
  final int? elementAtomicNumber;
  final Alignment imageAlignment;
  final double height;
  final BoxFit boxFit;

  const ImageHeader({
    super.key,
    required this.imageUrl,
    required this.gradient,
    required this.fallbackIcon,
    this.noImageMessage,
    this.noImageTitle,
    this.noImageExplanation,
    this.elementSymbol,
    this.elementAtomicNumber,
    this.imageAlignment = Alignment.center,
    this.height = 200,
    this.boxFit = BoxFit.cover,
  });

  @override
  State<ImageHeader> createState() => _ImageHeaderState();
}

class _ImageHeaderState extends State<ImageHeader> {
  // Wikimedia's on-demand thumbnail generation occasionally returns an HTML
  // error page with a 200 status instead of the image; flutter_cache_manager
  // caches that bad response as-is, so a plain rebuild would keep reusing it.
  // Evicting the cache entry before retrying forces a real network refetch.
  static const _maxRetries = 2;
  int _retryCount = 0;
  bool _retryScheduled = false;

  @override
  void didUpdateWidget(ImageHeader oldWidget) {
    super.didUpdateWidget(oldWidget);
    if (oldWidget.imageUrl != widget.imageUrl) {
      _retryCount = 0;
      _retryScheduled = false;
    }
  }

  void _scheduleRetry() {
    if (_retryScheduled || _retryCount >= _maxRetries || widget.imageUrl == null) return;
    _retryScheduled = true;
    DefaultCacheManager().removeFile(widget.imageUrl!).catchError((_) {});
    Future.delayed(const Duration(seconds: 2), () {
      if (!mounted) return;
      setState(() {
        _retryCount++;
        _retryScheduled = false;
      });
    });
  }

  Widget _loadingPlaceholder() => Container(
        height: widget.height,
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: widget.gradient),
        ),
        child: const Center(
          child: CircularProgressIndicator(color: Colors.white),
        ),
      );

  Widget _fallback() => Container(
        height: widget.height,
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: widget.gradient),
        ),
        child: widget.elementSymbol != null
            ? Center(
                child: Container(
                  width: 120,
                  padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 16),
                  decoration: BoxDecoration(
                    border: Border.all(color: Colors.white.withValues(alpha: 0.6), width: 2),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      if (widget.elementAtomicNumber != null)
                        Text(
                          '${widget.elementAtomicNumber}',
                          style: TextStyle(
                            color: Colors.white.withValues(alpha: 0.8),
                            fontSize: 13,
                            fontWeight: FontWeight.w500,
                          ),
                        ),
                      Text(
                        widget.elementSymbol!,
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 48,
                          fontWeight: FontWeight.bold,
                          height: 1.1,
                        ),
                      ),
                    ],
                  ),
                ),
              )
            : widget.noImageMessage != null
                ? Builder(
                    builder: (ctx) => GestureDetector(
                      onTap: widget.noImageExplanation != null
                          ? () => showDialog(
                                context: ctx,
                                builder: (dialogCtx) => AlertDialog(
                                  title: Text(widget.noImageTitle ?? ''),
                                  content: Text(widget.noImageExplanation!),
                                  actions: [
                                    TextButton(
                                      onPressed: () => Navigator.pop(dialogCtx),
                                      child: Text(AppLocalizations.of(ctx)!.closeButton),
                                    ),
                                  ],
                                ),
                              )
                          : null,
                      child: Padding(
                        padding: const EdgeInsets.all(24),
                        child: Center(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              Text(
                                widget.noImageMessage!,
                                textAlign: TextAlign.center,
                                style: const TextStyle(
                                  color: Colors.white,
                                  fontSize: 14,
                                  fontStyle: FontStyle.italic,
                                  height: 1.5,
                                ),
                              ),
                              if (widget.noImageExplanation != null) ...[
                                const SizedBox(height: 8),
                                Icon(
                                  Icons.info_outline_rounded,
                                  color: Colors.white.withValues(alpha: 0.7),
                                  size: 18,
                                ),
                              ],
                            ],
                          ),
                        ),
                      ),
                    ),
                  )
                : Icon(widget.fallbackIcon,
                    size: 60, color: Colors.white.withValues(alpha: 0.5)),
      );

  @override
  Widget build(BuildContext context) => ClipRRect(
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        child: widget.imageUrl != null
            ? CachedNetworkImage(
                key: ValueKey('${widget.imageUrl}#$_retryCount'),
                imageUrl: widget.imageUrl!,
                height: widget.height,
                width: double.infinity,
                fit: widget.boxFit,
                alignment: widget.imageAlignment,
                placeholder: (_, __) => _loadingPlaceholder(),
                errorWidget: (_, __, ___) {
                  if (_retryCount < _maxRetries) {
                    WidgetsBinding.instance.addPostFrameCallback((_) => _scheduleRetry());
                    return _loadingPlaceholder();
                  }
                  return _fallback();
                },
              )
            : _fallback(),
      );
}

import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

class ImageHeader extends StatelessWidget {
  final String? imageUrl;
  final List<Color> gradient;
  final IconData fallbackIcon;
  final String? noImageMessage;
  final Alignment imageAlignment;
  final double height;

  const ImageHeader({
    super.key,
    required this.imageUrl,
    required this.gradient,
    required this.fallbackIcon,
    this.noImageMessage,
    this.imageAlignment = Alignment.center,
    this.height = 200,
  });

  Widget _fallback() => Container(
        height: height,
        decoration: BoxDecoration(
          gradient: LinearGradient(colors: gradient),
        ),
        child: noImageMessage != null
            ? Padding(
                padding: const EdgeInsets.all(24),
                child: Center(
                  child: Text(
                    noImageMessage!,
                    textAlign: TextAlign.center,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 14,
                      fontStyle: FontStyle.italic,
                      height: 1.5,
                    ),
                  ),
                ),
              )
            : Icon(fallbackIcon,
                size: 60, color: Colors.white.withValues(alpha: 0.5)),
      );

  @override
  Widget build(BuildContext context) => ClipRRect(
        borderRadius: const BorderRadius.vertical(top: Radius.circular(24)),
        child: imageUrl != null
            ? CachedNetworkImage(
                imageUrl: imageUrl!,
                height: height,
                width: double.infinity,
                fit: BoxFit.cover,
                alignment: imageAlignment,
                placeholder: (_, __) => Container(
                  height: height,
                  decoration: BoxDecoration(
                    gradient: LinearGradient(colors: gradient),
                  ),
                  child: const Center(
                    child: CircularProgressIndicator(color: Colors.white),
                  ),
                ),
                errorWidget: (_, __, ___) => _fallback(),
              )
            : _fallback(),
      );
}

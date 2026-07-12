import 'package:flutter/material.dart';

enum SpotlightAnchor { favoritesTab, accountIcon, none }

class OnboardingStep {
  final SpotlightAnchor anchor;
  final double spotlightRadius;
  final String title;
  final String body;
  final bool isLast;

  const OnboardingStep({
    required this.anchor,
    required this.title,
    required this.body,
    this.spotlightRadius = 48,
    this.isLast = false,
  });

  Offset resolveCenter(Size screen, EdgeInsets padding) {
    return switch (anchor) {
      SpotlightAnchor.favoritesTab =>
        Offset(screen.width * 0.75, screen.height - 40),
      SpotlightAnchor.accountIcon =>
        Offset(screen.width - 36, padding.top + 52),
      SpotlightAnchor.none =>
        Offset(screen.width / 2, screen.height / 2),
    };
  }

  /// Whether the tooltip should appear above the spotlight.
  bool get tooltipAbove => anchor == SpotlightAnchor.favoritesTab;
}

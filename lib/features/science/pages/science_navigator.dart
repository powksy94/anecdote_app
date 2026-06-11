import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/hub_split_dialog.dart';
import 'science_living_page.dart';
import 'science_nonliving_page.dart';

abstract class ScienceNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.scienceHub,
        leftType: ContentType.scienceLivingHub,
        rightType: ContentType.scienceNonLivingHub,
        onSelectLeft: () {
          Navigator.pop(context);
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => ScienceLivingPage(adService: adService),
              transitionsBuilder: (_, animation, __, child) =>
                  FadeTransition(opacity: animation, child: child),
              transitionDuration: const Duration(milliseconds: 250),
            ),
          );
        },
        onSelectRight: () {
          Navigator.pop(context);
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => ScienceNonLivingPage(adService: adService),
              transitionsBuilder: (_, animation, __, child) =>
                  FadeTransition(opacity: animation, child: child),
              transitionDuration: const Duration(milliseconds: 250),
            ),
          );
        },
      ),
    );
  }
}

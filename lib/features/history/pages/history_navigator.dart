import 'package:flutter/material.dart';
import '../../../core/models/content_type.dart';
import '../../../core/services/ad_service.dart';
import '../../../core/widgets/cards/hub_split_dialog.dart';
import '../../../core/pages/sub_hub_page.dart';

abstract class HistoryNavigator {
  static Future<void> show(BuildContext context, AdService adService) {
    return showDialog(
      context: context,
      builder: (_) => HubSplitDialog(
        hubType: ContentType.historyHub,
        leftType: ContentType.historyEventsHub,
        rightType: ContentType.historyCivilizationsHub,
        onSelectLeft: () {
          Navigator.of(context, rootNavigator: true).pop();
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.historyEventsHub,
                categories: const [
                  ContentType.history,
                  ContentType.battle,
                  ContentType.diplomaticScandal,
                ],
                adService: adService,
              ),
              transitionsBuilder: (_, animation, __, child) =>
                  FadeTransition(opacity: animation, child: child),
              transitionDuration: const Duration(milliseconds: 250),
            ),
          );
        },
        onSelectRight: () {
          Navigator.of(context, rootNavigator: true).pop();
          Navigator.push(
            context,
            PageRouteBuilder(
              pageBuilder: (_, __, ___) => SubHubPage(
                hubType: ContentType.historyCivilizationsHub,
                categories: const [
                  ContentType.kingOfFrance,
                  ContentType.americanPresident,
                  ContentType.britishMonarch,
                  ContentType.ottomanSultan,
                  ContentType.chineseDynasty,
                ],
                adService: adService,
              ),
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

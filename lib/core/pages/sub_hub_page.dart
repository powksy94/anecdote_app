import 'package:flutter/material.dart';
import '../models/content_type.dart';
import '../../generated/app_localizations.dart';
import '../services/ad_service.dart';
import '../widgets/cards/subcategory_card.dart';
import 'content_page.dart';

class SubHubPage extends StatefulWidget {
  final ContentType hubType;
  final List<ContentType> categories;
  final AdService adService;

  const SubHubPage({
    super.key,
    required this.hubType,
    required this.categories,
    required this.adService,
  });

  @override
  State<SubHubPage> createState() => _SubHubPageState();
}

class _SubHubPageState extends State<SubHubPage> {
  void _navigate(ContentType type) {
    widget.adService.showInterstitialAd(onComplete: () {
      if (!mounted) return;
      Navigator.push(
        context,
        PageRouteBuilder(
          pageBuilder: (_, __, ___) => ContentPage(contentType: type),
          transitionsBuilder: (_, animation, __, child) =>
              FadeTransition(opacity: animation, child: child),
          transitionDuration: const Duration(milliseconds: 250),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final loc = AppLocalizations.of(context)!;
    final gradient = widget.hubType.gradient;

    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(widget.hubType.icon, size: 24),
            const SizedBox(width: 8),
            Flexible(
              child: Text(
                widget.hubType.localizedTitle(loc),
                overflow: TextOverflow.ellipsis,
              ),
            ),
          ],
        ),
        centerTitle: true,
        backgroundColor: Colors.transparent,
        elevation: 0,
        foregroundColor: Colors.white,
        leading: IconButton(
          icon: Container(
            padding: const EdgeInsets.all(8),
            decoration: BoxDecoration(
              color: Colors.white.withValues(alpha: 0.2),
              borderRadius: BorderRadius.circular(12),
            ),
            child: const Icon(Icons.arrow_back, size: 20),
          ),
          onPressed: () => Navigator.pop(context),
        ),
      ),
      body: Container(
        decoration: BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [
              gradient[0],
              gradient[1].withValues(alpha: 0.8),
              theme.colorScheme.surface,
            ],
            stops: const [0.0, 0.3, 0.6],
          ),
        ),
        child: SafeArea(
          child: ListView.builder(
            padding: const EdgeInsets.fromLTRB(20, 24, 20, 24),
            itemCount: widget.categories.length,
            itemBuilder: (context, index) => SubCategoryCard(
              type: widget.categories[index],
              onNavigate: () => _navigate(widget.categories[index]),
            ),
          ),
        ),
      ),
    );
  }
}

import 'package:flutter/material.dart';
import '../../../generated/app_localizations.dart';
import '../../models/content_type.dart';

class ContentAppBar extends StatelessWidget implements PreferredSizeWidget {
  final ContentType contentType;
  final bool isLoading;
  final VoidCallback onBack;
  final VoidCallback onRefresh;

  const ContentAppBar({
    super.key,
    required this.contentType,
    required this.isLoading,
    required this.onBack,
    required this.onRefresh,
  });

  @override
  Size get preferredSize => const Size.fromHeight(kToolbarHeight);

  Widget _roundedIcon(IconData icon) => Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: Colors.white.withValues(alpha: 0.2),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Icon(icon, size: 20),
      );

  @override
  Widget build(BuildContext context) {
    final loc = AppLocalizations.of(context)!;
    return AppBar(
      title: Row(mainAxisSize: MainAxisSize.min, children: [
        Icon(contentType.icon, size: 24),
        const SizedBox(width: 8),
        Flexible(
          child: Text(contentType.localizedTitle(loc), overflow: TextOverflow.ellipsis),
        ),
      ]),
      centerTitle: true,
      backgroundColor: Colors.transparent,
      elevation: 0,
      foregroundColor: Colors.white,
      leading: IconButton(
        icon: _roundedIcon(Icons.arrow_back),
        onPressed: onBack,
      ),
      actions: [
        if (!isLoading)
          IconButton(
            icon: _roundedIcon(Icons.refresh_rounded),
            onPressed: onRefresh,
          ),
      ],
    );
  }
}

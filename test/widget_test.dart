import 'package:flutter_test/flutter_test.dart';
import 'package:projet_app_annecdote/app.dart';

void main() {
  testWidgets('App smoke test', (WidgetTester tester) async {
    await tester.pumpWidget(const AnecdoteApp());
    expect(find.byType(AnecdoteApp), findsOneWidget);
  });
}

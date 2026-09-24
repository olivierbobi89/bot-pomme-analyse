import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Remplace les xxxxx par le nouveau token donné par BotFather
TOKEN = "8718017391:AAE4_B-eZV2X3QlFohugaw27MCTHMaOdLSw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "Bonjour ! Je suis ton bot d'analyse pour le jeu Pomme.\n\n"
        "Envoie /analyse suivi de tes cotes séparées par des espaces.\n"
        "Exemple : /analyse 1.20 2.50 1.80 4.10"
    )
    await update.message.reply_text(msg)

async def analyse(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Veuillez fournir des valeurs. Exemple : /analyse 1.20 2.50 1.80")
        return

    try:
        data = [float(x.replace(',', '.')) for x in context.args]
    except ValueError:
        await update.message.reply_text("Format invalide. Envoyez uniquement des nombres.")
        return

    total = len(data)
    moyenne = sum(data) / total
    minimum = min(data)
    maximum = max(data)
    
    plus_de_2 = sum(1 for x in data if x >= 2.0)
    pct_plus_de_2 = (plus_de_2 / total) * 100

    rapport = (
        f"📊 **Analyse des {total} parties**\n\n"
        f"• **Moyenne :** {moyenne:.2f}\n"
        f"• **Minimum :** {minimum:.2f}\n"
        f"• **Maximum :** {maximum:.2f}\n"
        f"• **Cotes >= 2.00 :** {plus_de_2}/{total} ({pct_plus_de_2:.1f}%)\n\n"
        f"⚠️ *Analyse statistique indicative, aucun gain n'est garanti.*"
    )
    await update.message.reply_text(rapport, parse_mode='Markdown')

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analyse", analyse))
    app.run_polling()

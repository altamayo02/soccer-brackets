from model.Cup import Cup


def main():
	c = Cup("./src/soccer-brackets/view/ui/soccer-teams.ui")
	c.get_ui().show()

if __name__ == "__main__":
	main()
def output(lock, message):
    lock.acquire()
    print(message)
    lock.release()


def loop_menu(lock, subject, options):

    action = None
    while action is None:
        output(lock, "Select " + subject + "('e' to exit): ")

        for idx, o in enumerate(options, start=1):
            output(lock, str(idx) + ": " + o + "")

        try:
            action = input()
        except SyntaxError:
            action = None

        if action is None:
            output(lock, "Please select an option")
        elif action == 'e':
            return None
        else:
            try:
                selected = int(action)
            except ValueError:
                output(lock, "A number is required")
                continue
            else:
                if selected > len(options):
                    output(lock, "Option " + str(selected) + " not available")
                    action = None
                    continue
                else:
                    return selected

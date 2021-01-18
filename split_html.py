import sys

if __name__ == '__main__':
    # Take string from STDIN and split it into multiple HTML documents

    index = 0
    f = open(f'docs/{index}.html', 'w')
    for line in sys.stdin:
        if '|' == line.rstrip():
            # Close the current file and begin writing the next one
            f.close()
            index += 1
            f = open(f'html/{index}.html', 'w')
            continue
        # Write the line to the current file
        f.write(line)

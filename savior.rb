# a script i (mostly) wrote to convert all print statements in the project to use a method in base.
# andreberg wrote the regex magic, and that on its own can be found on his gist here: https://gist.github.com/andreberg/5637758


def convert_to_py3k_print(text)
  regex_print_descriptor = /print(\s*)>>(\s*)(.+),\s*(.+)/
  regex_print_simple = /print\s+(?![\'\"])([^#\n\r]+(?<! ))?/
  regex_print_multiline = /print\s+(ur|ru)?(['"]{1,3})([\w\W]+?)(\2)([^#\n\r]+(?<! ))?/m
  regex_print = /print\s+(ur|ru)?(['"])(?!\2)([^\r\n]+)(\2)([^#\n\r]+(?<! ))?/
  result = text.gsub(regex_print_descriptor, "print(\\4, file=\\3)")
  result.gsub!(regex_print, "base.put(\\1\\2\\3\\4\\5)")
  result.gsub!(regex_print_simple, "base.put(\\1)")
  result.gsub!(regex_print_multiline, "base.put(\\1\\2\\3\\4\\5)")
  result
end

Dir['**/*'].each do |f|
# f = 'test.txt'
  text = ''
  if not File.directory? f and f[-3,3] == '.py' then
    puts f
    File.open(f,'r+') do |file|
      text = file.read
    end
    File.open(f,'w') do |file|
      # file.read
      file.puts convert_to_py3k_print(text)
    end
  end
end

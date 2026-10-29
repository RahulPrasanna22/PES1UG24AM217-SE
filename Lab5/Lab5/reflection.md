# Reflection

The supplied handout contains no reflection questions on its three pages, although the README asks for four answers. These responses address four common reflection prompts for the static-analysis lab.

1. **What is static code analysis, and why is it useful?**  
   Static analysis checks source code without running it. It catches likely defects, unsafe patterns, and style problems early, making review more consistent and reducing the chance that issues reach users.

2. **What did the tools find, and which finding mattered most?**  
   Bandit found unsafe temporary-file creation and a shell-injection risk in the ping helper. Pylint identified the mutable default list, broad exception handling, and naming/documentation problems; Flake8 identified whitespace issues. The shell invocation mattered most because an address could be interpreted as shell syntax.

3. **What was challenging about interpreting and fixing the findings?**  
   A warning needs context: the ping helper was unused by the demo, but its command execution still created risk. Fixing the mutable default also required preserving the optional history behavior. Understanding the helper contracts helped keep the fixes useful.

4. **How did static analysis improve the program, and what are its limits?**  
   The tools made security risks, error handling, names, and formatting visible and provided repeatable checks after changes. They do not prove the program is correct or cover every runtime case, so manual review and execution remain useful.
